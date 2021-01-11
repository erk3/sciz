#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being_troll_private import TrollPrivate
import os, re
import modules.globals as sg


# CLASS DEFINITION
class Notifier:

    # Constructor
    def __init__(self):
        self.check_conf()

    # Configuration loader and checker
    def check_conf(self):
        # No conf needed yet
        pass

    @staticmethod
    def eval_attrs(o, attrs):
        # Evaluate attributes
        for key in attrs:
            prefix = attrs[key][sg.CONF_FORMAT_ATTRS_PREFIX] if sg.CONF_FORMAT_ATTRS_PREFIX in attrs[key] else ''
            suffix = attrs[key][sg.CONF_FORMAT_ATTRS_SUFFIX] if sg.CONF_FORMAT_ATTRS_SUFFIX in attrs[key] else ''
            time = attrs[key][sg.CONF_FORMAT_ATTRS_TIME] if sg.CONF_FORMAT_ATTRS_TIME in attrs[key] else None
            try:
                if time is not None:
                    attr = eval('f"%s"' % attrs[key][sg.CONF_FORMAT_ATTRS_ATTR].replace('}', ':' + time + '}'))
                else:
                    attr = eval('f"%s"' % attrs[key][sg.CONF_FORMAT_ATTRS_ATTR])
            except (AttributeError, TypeError) as e:
                attr = ''
            value = attrs[key][sg.CONF_FORMAT_ATTRS_VALUE] if sg.CONF_FORMAT_ATTRS_VALUE in attrs[key] else attr
            res = prefix + value + suffix if attr not in ['None', 'False', ''] else ''
            setattr(o, key, res)
        return o

    @staticmethod
    def build_computed_attrs(o, builded_attrs):
        for key in builded_attrs:
            builded = builded_attrs[key]
            real_matches = 0
            res = re.finditer(r'(?P<replace>{(?P<attr>[^{}]+)})', builded)
            if res is not None:
                for item in res:
                    to_replace = item.groupdict()['replace']
                    attr = item.groupdict()['attr']
                    attr_replace = ''
                    if hasattr(o, attr) and getattr(o, attr) not in [None, '']:
                        attr_replace = getattr(o, attr)
                        real_matches += 1 if len(attr_replace) > 1 else 0  # Don't add things like separators
                    builded = builded.replace(to_replace, attr_replace)
            if real_matches < 1:
                builded = ''
            setattr(o, key, builded)
        return o

    # STRINGIFY (Do not change the naming of the 'o' parameter without changing it accordingly in the formats...)
    def stringify(self, o, json=None, filters=None, stringifyTrollCapa=True):
        notification = ''
        # check we have a format
        if json is None and sg.format is not None:
            json = sg.format
        elif json is None:
            return ''
        # Get all the format section corresponding (name of the current class and names of the parent classes)
        sections = [type(o).__name__]
        for base in o.__class__.__bases__:
            if base.__name__ != 'Base':
                sections.insert(0, base.__name__)
        for section in sections:
            # Evaluate attributes
            attrs = json[section][sg.CONF_FORMAT_ATTRS]
            o = self.eval_attrs(o, attrs)
            # Build the computed attrs and at the end the final notification
            builded_attrs = json[section][sg.CONF_FORMAT_BUILDED_ATTRS] if sg.CONF_FORMAT_BUILDED_ATTRS in json[
                section] else {}
            o = self.build_computed_attrs(o, builded_attrs)
            # Fix the final notification
            notif_format = json[section][sg.CONF_FORMAT_NOTIFICATION]
            o = self.build_computed_attrs(o, {sg.CONF_FORMAT_NOTIFICATION: notif_format})
            notification = getattr(o, sg.CONF_FORMAT_NOTIFICATION)
            # Delete nested parenthesis
            left, right, i = [], [], 0
            while i < len(notification):
                if notification[i] == '(':
                    left.append(i)
                elif notification[i] == ')':
                    right.append(i)
                if len(left) == len(right):
                    if len(left) > 1:
                        d = 0
                        for dl in left[1:]:
                            notification = notification[:dl - d] + notification[dl - d + 1:]
                            d += 1
                            right = list(map(lambda x: x - 1 if x > dl else x, right))
                        d = 0
                        for rl in right[:-1]:
                            notification = notification[:rl - d] + notification[rl - d + 1:]
                            d += 1
                    left, right = [], []
                i += 1
            # Fix others things
            notification = re.sub(r'(\((\W|\s)*\)|\)\()', ' ', notification) # Delete empty parenthesis and merge glued parenthesis
            notification = re.sub(r'\s+\)', ')', notification).strip() # Delete unecessary whitespaces before end parenthesis
            notification = re.sub(r'\(\s+', '(', notification).strip() # Delete unecessary whitespaces after start parenthesis
            notification = re.sub(r'\s+', ' ', notification).strip() # Delete unecessary whitespaces
            notification = re.sub(r'\s+(\W)+?\s+', r' \1 ', notification) # Delete multiple separators like ;; or ::
            notification = re.sub(r'([^\w\)\s\]\[\+\-\'\!\%])\s*\((.+?)\)', r'\1 \2', notification)  # Delete parenthesis after a separator
            notification = re.sub(r'(\\n\s*(\\n)*)+', os.linesep, notification) # Transform lineseparator and delete unecessary ones
            notification = re.sub(r'\n$', '', notification) # Delete last lineseparator
            # Apply abbreviations
            abreviations = json[sg.CONF_FORMAT_ABREVIATIONS]
            for key in abreviations:
                notification = notification.replace(key, abreviations[key])
        # If we are stringifying a Troll, then stringify its capas
        if isinstance(o, TrollPrivate) and stringifyTrollCapa:
            for capa in o.troll_privates_capas:
                notification += '\n' + self.stringify(capa, json, filters)
        # Filter out things
        if filters is not None:
            filters = [sg.flatten(f) for f in filters]
            notification_splitted = notification.split('\n')
            if len(notification_splitted) > 1:
                res = [line for line in notification_splitted[1:] if any(f in sg.flatten(line) for f in filters)]
                if len(res) > 0:
                    notification = notification_splitted[0] + '\n' + '\n'.join(res)
                else:
                    notification = ''
        return notification
