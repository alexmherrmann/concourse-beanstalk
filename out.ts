#!/usr/bin/env ts-node-esm
import { wrapOut } from 'concourse-node-helper';
import { ElasticBeanstalk } from '@aws-sdk/client-elastic-beanstalk';
import { S3 } from '@aws-sdk/client-s3';

wrapOut<{
    aws_access_key_id: string,
    aws_secret_access_key: string,
    aws_region: string,
    application_name: string,
}, {
    version_label: string,
    bucket: string,
    key: string,
}>(async (input, ctx) => {
    // check for all the source params
    for (const param of ['aws_access_key_id', 'aws_secret_access_key', 'aws_region', 'application_name']) {
        if (!input.source[param]) {
            throw new Error(`Missing required source param: ${param}`);
        }
    }

    // Check for all the params
    for (const param of ['version_label', 'bucket', 'key']) {
        if (!input.params[param]) {
            throw new Error(`Missing required param: ${param}`);
        }
    }


    const ebClient = new ElasticBeanstalk({
        region: input.source.aws_region,
        credentials: {
            accessKeyId: input.source.aws_access_key_id,
            secretAccessKey: input.source.aws_secret_access_key
        }
    });

    try {

        const previouslyMade = await ebClient.describeApplicationVersions({
            ApplicationName: input.source.application_name,
            VersionLabels: [input.params.version_label]
        });

        if (previouslyMade.ApplicationVersions?.length ?? 0 > 0) {
            ctx.logit(`Version ${input.params.version_label} already exists, skipping`);
            return {
                version: {
                    ...input.version,
                    ref: previouslyMade.ApplicationVersions?.[0].VersionLabel ?? ''
                }
            }
        } else {
            const created = await ebClient.createApplicationVersion({
                ApplicationName: input.source.application_name,
                VersionLabel: input.params.version_label,
                SourceBundle: {
                    S3Bucket: input.params.bucket,
                    S3Key: input.params.key
                }
            });

            return {
                version: {
                    ...input.version,
                    ref: `${created.ApplicationVersion?.VersionLabel}`
                }
            }
        }
    } catch (e) {
        ctx.logit(`Error creating version: ${e.message}`);
        throw e;
    }

})()