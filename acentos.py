#!/usr/bin/env python3
# encoding: utf-8

import html.entities
s = 'pétala não à vê saúde sã cântaro'

table = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}

a = s.translate(table)

print(a)

#'Voilà'.translate(table)

  
