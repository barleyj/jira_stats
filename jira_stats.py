from os import environ as env

from jira import JIRA
from pandas import Series, DataFrame


options = {'server': ''}

jira_client = JIRA(options, basic_auth=(env['JIRA_USERNAME'], env['JIRA_TOKEN']))

team = ''
start_date = ''

issues = [i for i in jira_client.search_issues('team = "{}" AND resolved >= {}'.format(team, start_date), maxResults=1100) if 'customfield_10002' in i.raw['fields'] and 'customfield_10005' in i.raw['fields'] and i.raw['fields']['customfield_10005']]

story_points = Series([i.raw['fields']['customfield_10002'] for i in issues])

story_point_counts = story_points.value_counts()

indexed_story_point_counts = story_point_counts.sort_index()

df = DataFrame(indexed_story_point_counts)
plt = df.plot(kind='bar', legend=False, title='Count of tickets by Story Points')
plt.set_xlabel('Story Points')
plt.set_ylabel('Ticket Count')
fig = plt.get_figure()
fig.savefig('./story_points.png')

for story_point in indexed_story_point_counts.keys():
    sprints = Series([len(i.raw['fields']['customfield_10005']) for i in issues if i.raw['fields']['customfield_10002'] == story_point])
    sprint_counts = sprints.value_counts()

    indexed_sprint_counts = sprint_counts.sort_index()

    df = DataFrame(indexed_sprint_counts)
    title = 'Sprints taken for {} story points'.format(int(story_point))
    plt = df.plot(kind='bar', legend=False, title=title)
    plt.set_xlabel('Sprint Count')
    plt.set_ylabel('Ticket Count')
    fig = plt.get_figure()
    fig.savefig('./sprints-{}.png'.format(int(story_point)))
    
