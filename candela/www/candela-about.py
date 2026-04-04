# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""Candela About page — public, no login required."""
no_cache = 1

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = False
    context.title = "About Candela Restaurant"
