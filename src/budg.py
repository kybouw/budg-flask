#! /usr/bin/python3
"""
budg

Budgeting income the easy way

by Kyle Bouwman

Copyright (C) 2022-2023 Kyle Bouwman

This file is part of budg.

budg is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

budg is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with budg.  If not, see <https://www.gnu.org/licenses/gpl.html>.
"""
import argparse
import math
import os
import re
import sys
import tomllib
from typing import Any

PLAN_DIRECTORY = os.path.join(os.path.expanduser("~"), "Documents", "budg")


def make_budg_table(plan: dict[str, Any], budg_total: float) -> str:
    """Creates output text using calculated budget amounts based on plan
    for the given total

    Parameters
    ----------
    plan: dict[str, Any]
        A plan object
    budg_total: float
        The total amount to budget

    Returns
    -------
    str
        Formatted string with calculated budget values
    """
    # plans follow a major/minor format
    # There is major category that labels groups of budget categories,
    #   and a minor category that labels individual budget categories
    s = "=============================\n"
    for major in plan:
        # if major has no minor categories
        major_type: type = type(plan[major])
        if major_type is float or major_type is int:
            major_ratio = float(plan[major] / 100)
            major_amount = budg_total * major_ratio
            trunc_major_amount = math.floor(major_amount * 100) / 100
            formatted_amount = f"{trunc_major_amount:.2f}"
            s += f"{major:19}${formatted_amount:>9}\n"

        # if major is group of minor categories
        elif major_type is dict:
            major_sum_amount: float = 0
            # add placeholder for total at the end
            s += "00000000000000000000000000000\n"
            s += "-----------------------------\n"
            for category in plan[major]:
                # for backwards compatibility, skip "total" minor
                if str.lower(category) == "total":
                    continue
                # calculate the value of this category
                ratio = plan[major][category] / 100
                value = budg_total * ratio
                # truncate
                trunc_factor = 100
                trunc_value = math.floor(value * trunc_factor) / trunc_factor
                major_sum_amount += trunc_value
                # add to string
                value_formatted = f"{trunc_value:.2f}"
                s += f"> {category:17}${value_formatted:>9}\n"
            major_sum_formatted = f"{major_sum_amount:.2f}"
            # swap out placeholder for total major amount
            s = str.replace(
                s,
                "00000000000000000000000000000",
                f"{major:19}${major_sum_formatted:>9}",
            )
        s += "=============================\n"
    return s


def get_dollar_value(val_str: str) -> float:
    """Converts input to a float if it can be interpreted as a
    valid dollar amount. Returns 0 if input does not follow
    rules defined below.

    - Strings must not contain alphabet characters:
        123.45 or 123
        - 5e2 is not acceptable. Must be 500.
    - Strings may start with a dollar sign (USD only):
        $123.45 or $123
    - Strings may separate thousands groups with commas:
        123,456.78 or 1,200
        - comma groups must be groups of threes. No 1234,567 or 123,45
    - Values less than a dollar must start with a 0 before the decimal:
        0.32
    - Strings may only contain up to two decimal places:
        123.45
        - 5.5 is acceptable but will be interpreted as 5.50, not 5.05

    Parameters
    ----------
    val_str: str
        A string that represents a dollar amount

    Returns
    -------
    float
        A dollar amount as a float. Zero if string value does not follow
        format defined above.
    """
    # regex for recognizing dollar amount patterns as defined above
    dollar_amount_pattern = re.compile(
        pattern=r"^\$?(((\d{1,3}(,\d{3})*)|(\d+))(\.\d{0,2})?)$",
    )
    val_float: float = 0

    if re.fullmatch(dollar_amount_pattern, val_str) is not None:
        # string matches rules
        # remove $ and , and cast float
        no_commas = str.replace(val_str, ",", "")
        no_dollarsigns = str.replace(no_commas, "$", "")
        val_float = float(no_dollarsigns)
    else:
        # string does not match rules
        print(f"Could not interpret value: {val_str}")
        print("Try using a value in the form XXX.XX")
        if str.startswith(val_str, "."):
            print(
                "Values less than 1 must start with a 0",
                "\n e.g., .32 -> 0.32",
            )
        print()

    return val_float

def calculate(plan: str, amount: float) -> str:
    toml_dict = tomllib.loads(plan)
    table = make_budg_table(toml_dict, amount)
    return table
