#!/usr/bin/env python3

import sys
from ruamel.yaml import YAML
import re

in_path = sys.argv[1]
out_dir = sys.argv[2]

print('Reading %s' % in_path)
with open(in_path) as in_file:
    yaml = YAML()
    in_rules = yaml.load(in_file)

    if 'spec' in in_rules:
        rule_groups = in_rules['spec']['groups']
    else:
        rule_groups = in_rules['groups']

    for in_rule in rule_groups:
        item_name = in_rule['name']
        print(' - %s' % item_name)
        alerts = []
        rules = []

        for item in in_rule['rules']:
            if 'alert' in item:
                alerts.append(item)
            else:
                rules.append(item)

        if alerts:
            alert_name = re.sub('[-.](alerts|rules)', '',
                                item_name) + ".alerts"
            print(' -----> %s with %d alerts' % (alert_name, len(alerts)))
            alerts_path = '%s/%s.yaml' % (out_dir, alert_name)
            out_alerts = {'name': alert_name, 'rules': alerts}
            with open(alerts_path, 'w') as out_file:
                yaml.dump([out_alerts], out_file)

        if rules:
            rule_name = re.sub('[-.](alerts|rules)', '', item_name) + ".rules"
            print(' -----> %s with %d rules' % (rule_name, len(rules)))
            rules_path = '%s/%s.yaml' % (out_dir, rule_name)
            out_rules = {'name': rule_name, 'rules': rules}
            with open(rules_path, 'w') as out_file:
                yaml.dump([out_rules], out_file)
