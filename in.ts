#!/usr/bin/env ts-node-esm
import { wrapIn } from 'concourse-node-helper';

wrapIn<{}>(async ({ version }) => ({ version }))()