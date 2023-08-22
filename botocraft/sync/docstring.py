from dataclasses import dataclass, field
import re
from textwrap import wrap
from typing import Optional, List, Tuple, Literal

import botocore.model
from markdownify import markdownify


@dataclass
class FormatterArgs:

    line_range: Optional[Tuple[int, int]] = None
    length_range: Optional[Tuple[int, int]] = None
    black: bool = True
    style: Literal['sphinx', 'epytext'] = 'sphinx'
    force_wrap: bool = False
    make_summary_multi_line: bool = True
    pre_summary_newline: bool = True
    post_summary_newline: bool = True
    post_description_blank: bool = False
    non_strict: bool = False
    rest_section_adorns: str = r'''[!\"#$%&'()*+,-./\\:;<=>?@[]^_`{|}~]{4,}'''
    tab_width: int = 4
    wrap_summaries: int = 79
    wrap_descriptions: int = 79
    non_cap: List[str] = field(default_factory=list)


class DocumentationFormatter:

    MARKDOWN_LINK_RE = re.compile(
        r"(?:\[(?P<text>.*?)\])\((?P<link>.*?)\)",
        re.MULTILINE | re.DOTALL
    )

    def __init__(self, max_length: int = 79):
        #: Wrap lines at this length.
        self.max_length = max_length

    def _clean_uls(self, documentation: str) -> str:
        """
        Look through ``documentation`` for unordered lists and clean them up.

        This means wrapping them properly at 79 characters, and adding a blank
        line before and after.

        Args:
            documentation: the partially processed reStructuredText
                documentation

        Returns:
            The documentation with unordered lists cleaned up.
        """
        lines = []
        source_lines = documentation.split('\n')
        for i, line in enumerate(source_lines):
            if line.startswith('*'):
                previous_line = source_lines[i - 1]
                if previous_line.strip() != '' and not previous_line.startswith('*'):
                    lines.append('')
                if len(line) > self.max_length:
                    wrapped = wrap(line, self.max_length)
                    lines.append(wrapped[0])
                    lines.extend([f'  {line}' for line in wrapped[1:]])
                else:
                    lines.append(line)
            else:
                if len(line) > self.max_length:
                    lines.extend(wrap(line, self.max_length))
                else:
                    lines.append(line)
        return '\n'.join(lines)

    def _clean_links(self, documentation: str) -> str:
        """
        Transform our Markdown links to reStructuredText links.

        Args:
            documentation: the partially processed reStructuredText
                documentation

        Returns:
            The documentation with links cleaned up.
        """
        for match in self.MARKDOWN_LINK_RE.finditer(documentation):
            text = match.group('text')
            link = match.group('link')
            link = link.replace(' ', '')
            documentation = documentation.replace(match.group(0), f'`{text} <{link}>`_')
        return documentation

    def clean(self, documentation: str, max_lines: Optional[int] = None) -> str:
        """
        Take the input documentation in HTML format and clean it up for use in a
        docstring, as reStructuredText.

        Args:
            documentation: the HTML documentation to clean up

        Returns:
            Properly formatted reStructuredText documentation.
        """
        documentation = markdownify(documentation)
        if max_lines is not None:
            documentation = '\n'.join(documentation.split('\n')[:max_lines])
        if '\n' in documentation:
            documentation = '\n'.join([line.strip() for line in documentation.split('\n')])
        documentation = documentation.replace('`', '``')
        documentation = self._clean_uls(documentation)
        documentation = self._clean_links(documentation)
        return documentation

    def format_docstring(self, shape: botocore.model.Shape) -> str:
        """
        Format the documentation for a model.

        Args:
            shape: the botocore shape for the model

        Returns:
            The formatted documentation for the model as reStructuredText.
        """
        documentation = shape.documentation
        documentation = self.clean(documentation)
        return documentation

    def format_attribute(self, docs: str) -> str:
        """
        Format the documentation for a single attribute of a model.

        Args:
            shape: the botocore shape for the attribute

        Returns:
            The formatted documentation for the attribute as reStructuredText.
        """
        documentation = docs
        documentation = self.clean(documentation, max_lines=1)
        lines = wrap(documentation, self.max_length)
        return '\n'.join([f'    #: {line.strip()}' for line in lines])
