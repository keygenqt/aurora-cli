### Changeln template example
### Template engine is Mako - https://www.makotemplates.org/
### Base template format is Markdown - https://python-markdown.github.io/
###
### Show all values: 
### ${context.keys()}
### ${context.__dict__}
###
### Structure:
### ln_date: datetime
### ln_last: str
### ln_list_tags: [TagReference]
### ln_count_tags: int
### ln_group_commits: [
###     name: str, 
###     date: datetime,
###     commits: [Commit],
###     group: [
###             {
###                 name: str, 
###                 commits: [
###                     {
###                         commit: Commit, 
###                         regex: [], 
###                         clean: str
###                     }
###                 ]
###             }
###          ]
###     ]

<%! from datetime import datetime %>

${"##"} Updated: ${ln_date.strftime('%m/%d/%Y %H:%M:%S %p')}

${"##"} Info

- Last tag: ${ln_last}
- Released: ${ln_count_tags}

${"##"} Versions
% for item in ln_list_tags:
- Version: ${item.name} (${datetime.fromtimestamp(item.commit.committed_date).strftime('%d/%m/%Y')})
% endfor

% for tag in ln_group_commits:

    % if tag['commits']:
        % if tag['name'] == 'HEAD':
            ${"###"} HEAD (${ln_date.strftime('%d/%m/%Y')})
        % else:
            ${"###"} Version: ${tag['name']} (${datetime.fromtimestamp(tag['date']).strftime('%d/%m/%Y')})
        % endif
    % endif

    % for group in tag['group']:

        % if group['commits']:
            ${"####"} ${group['name']}

            % for commit in group['commits']:
                - ${commit['clean']}
            % endfor
        % endif

    % endfor
% endfor

