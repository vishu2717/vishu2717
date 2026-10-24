#!/usr/bin/env python3
import os
import sys
import json
import re
import urllib.request

def main():
    token = os.environ.get("METRICS_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: No GitHub token provided in environment.", file=sys.stderr)
        sys.exit(1)
    
    if token.startswith("token-"):
        token = token[len("token-"):]

    query = '''
    query {
      user(login: "vishu2717") {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                color
                weekday
              }
            }
          }
        }
      }
    }
    '''

    req = urllib.request.Request(
        'https://api.github.com/graphql',
        data=json.dumps({'query': query}).encode('utf-8'),
        headers={'Authorization': f'bearer {token}', 'User-Agent': 'Python'}
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    cal = data['data']['user']['contributionsCollection']['contributionCalendar']
    weeks = cal['weeks']

    values = []
    max_c = 0
    current_streak = 0
    best_streak = 0

    for w in weeks:
        for d in w['contributionDays']:
            c = d['contributionCount']
            values.append(c)
            max_c = max(max_c, c)
            if c > 0:
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 0

    avg = f'{sum(values) / len(values):.2f}'.rstrip('0').rstrip('.')
    reference = max_c
    size = 6

    path = '.github/assets/metrics-activity.svg'
    if not os.path.exists(path):
        print(f"File {path} not found.")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update streak & stats text
    content = re.sub(r'Current streak \d+ days', f'Current streak {current_streak} days', content)
    content = re.sub(r'Best streak \d+ days', f'Best streak {best_streak} days', content)
    content = re.sub(r'Highest in a day at \d+', f'Highest in a day at {max_c}', content)
    content = re.sub(r'Average per day at ~[\d\.]+', f'Average per day at ~{avg}', content)

    # Generate grid
    grid_svg = '<g transform="scale(4) translate(12, 0)">\n'
    for i, week in enumerate(weeks):
        grid_svg += f'<g transform="translate({i * 1.7:.1f}, {i})">\n'
        for j, day in enumerate(week['contributionDays']):
            count = day['contributionCount']
            color = day['color']
            ratio = (count / reference) if reference else 0
            y_trans = j + (1 - ratio) * size
            h = ratio * size
            if count == 0:
                grid_svg += f'''    <g transform="translate({j * -1.7:.1f}, {y_trans:.1f})">
        <path fill="{color}" d="M1.7,2 0,1 1.7,0 3.4,1 z"/>
        <path fill="{color}" filter="url(#brightness1)" d="M0,1 1.7,2 1.7,2 0,1 z"/>
        <path fill="{color}" filter="url(#brightness2)" d="M1.7,2 3.4,1 3.4,1 1.7,2 z"/>
    </g>\n'''
            else:
                grid_svg += f'''    <g transform="translate({j * -1.7:.1f}, {y_trans})">
        <path fill="{color}" d="M1.7,2 0,1 1.7,0 3.4,1 z"/>
        <path fill="{color}" filter="url(#brightness1)" d="M0,1 1.7,2 1.7,{2 + h} 0,{1 + h} z"/>
        <path fill="{color}" filter="url(#brightness2)" d="M1.7,2 3.4,1 3.4,{1 + h} 1.7,{2 + h} z"/>
    </g>\n'''
        grid_svg += '</g>\n'
    grid_svg += '</g>'

    pattern = r'<g transform="scale\(4\) translate\(12, 0\)">.*?</g>\s*</svg>'
    content = re.sub(pattern, grid_svg + '\n                </svg>', content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {path} successfully! Current streak: {current_streak}, Best: {best_streak}, Max: {max_c}, Avg: {avg}")

if __name__ == "__main__":
    main()
