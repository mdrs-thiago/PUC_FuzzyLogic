import pandas as pd
import numpy as np
import skfuzzy as fuzz
import sympy as sp
from skfuzzy import control as ctrl

def select_higher_membership(linguistic_variable, input_value):
    p = 0
    label_max = None
    input_value = np.clip(input_value, linguistic_variable.universe.min(), linguistic_variable.universe.max())
    for label, set in linguistic_variable.terms.items():
        pertinence = fuzz.interp_membership(linguistic_variable.universe, set.mf, input_value)
        if pertinence > p:
            label_max = label 
            p = pertinence 
    return label_max, p

def create_rule(list_values, list_variables, n_outputs = 1):
    rule_p = 1
    list_antecedents = []
    list_consequents = []
    for i in range(len(list_variables) - n_outputs):
        label, p = select_higher_membership(list_variables[i], list_values[i])
        rule_p *= p
        list_antecedents.append(list_variables[i][label])
    for k in range(n_outputs):
        label, p = select_higher_membership(list_variables[i+k+1], list_values[i+k+1])
        list_consequents.append(list_variables[i+k+1][label])
        rule_p *= p
    return [list_antecedents, list_consequents, rule_p]

def create_rules(df, list_variables, n_outputs=1):
    rule_list = []
    for i in range(len(df)):
        rule_list.append(create_rule(df.iloc[i], list_variables, n_outputs))
    return rule_list

def filter_rules(list):
    list_filtered = []
    for i in range(len(list)):
        if list[i][0] not in [x[0] for x in list_filtered]:
            list_filtered.append(list[i])
        else:
            for j in range(len(list_filtered)):
                if list_filtered[j][0] == list[i][0]:
                    if list_filtered[j][2] < list[i][2]:
                        list_filtered[j] = list[i]
    return list_filtered

def create_fuzzy_rules(rules):
    list_rules = []
    for rule in rules:
        combined_antecedent = rule[0][0]
        for element in rule[0][1:]:
            combined_antecedent &= element
        combined_consequent = rule[1][0]
        for element in rule[1][1:]:
            combined_consequent &= element
        list_rules.append(ctrl.Rule(combined_antecedent, combined_consequent))
    return list_rules

def create_fuzzy_system(df, list_variables, n_outputs=1):
    rules = create_rules(df, list_variables, n_outputs)
    rules = filter_rules(rules)
    rules = create_fuzzy_rules(rules)
    return ctrl.ControlSystem(rules)
