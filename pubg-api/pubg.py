"""
Simple PUGB API wrapper to collect PUBG match statistics or player statistics
"""

import requests
import config
import json
import pandas as pd
import time
from tqdm import tnrange, tqdm
import sys

pd.options.display.max_columns = 200
pd.options.display.max_rows = 200

def _base_url(path):
    base_url = config.BASE_URL
    return base_url + '/' + path 

def _platform_url(platform=None):
    if platform is None:
        return _base_url('steam')
    return _base_url(platform)

def _fetch(url):
    headers = {
        "Authorization" : config.API_KEY,
        "Accept" : "application/vnd.api+json",
        "Accept-Encoding":"gzip"
    }
    return requests.get(url, headers=headers)

def get_content(url=None, verbose=True):
    if url is None:
        raise ValueError('Parameter `url` must be a non-nil reference')
    
    if verbose:
        print(f'Fetching URL : {url}')
    resp = _fetch(url)
    # Check HTTP response
    if resp.status_code != 200:
        if resp.status_code == 401:
            raise ValueError('API key invalid or missing')
        elif resp.status_code == 404:
            raise ValueError('The specified resource was not found')
        elif resp.status_code == 415:
            raise ValueError('Content type incorrect or not specified')
        # If you exceed the rate limit, go to sleep
        elif resp.status_code == 429:
            print('Too many requests made, go to sleep now (~_~)zzz..!')
            time.sleep(4000)
    # Get JSON from API request
    try:    
        resp_json = json.loads(resp.content.decode())
    except Exception as ex:
        # Sometimes you may get UnicodeDecode error
        print("Unexpected error:", sys.exc_info()[0])
        raise
    # Get rate limit info only affects certain endpoints
    if verbose:
        try:
            api_rate_limit = resp.headers['X-Ratelimit-Limit']
            api_remaining = resp.headers['X-Ratelimit-Remaining']
            posix_timestamp = int(resp.headers['X-Ratelimit-Reset'])
            reset_time = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(posix_timestamp))
            print('---------- API RATE LIMIT INFO -------------')
            print(f'Request Remaining: {api_remaining}/{api_rate_limit}')
            print(f'Reset Time: {reset_time}')
        except:
            pass
    return resp_json

def get_match_samples(platform=None, verbose=True):
    # Make platform API endpoint
    url = _platform_url(platform)
    url += '/samples'
    # Make API request
    data = get_content(url, verbose=verbose)["data"]
    # Get sample matches from the JSON
    matches = data['relationships']['matches']['data']
    if verbose:
        print(f'Found {len(matches)} number of matches')
    return pd.Series([match['id'] for match in matches], name='match_id')

def get_match_stats(matches=None, platform=None):
    # Verify the parameter is passed
    if matches is None:
        raise ValueError('You forgot to pass parameter `matches`')
    if not isinstance(matches, pd.Series):
        raise TypeError('Wrong data type!, parameter `matches` should be a Pandas Series data type')

    # Setup match endpoint
    url = _platform_url(platform)
    url += '/matches/'
    
    # Convert matches to python list
    matches_list = matches.tolist()
    n_matches = len(matches_list)
    
    # Store PUBG stats of sample matches
    pubg_stats = []
    
    # Loop through match list and store player stats
    # Create progress bar to keep track
    progress_bar = tqdm(enumerate(matches_list), desc='Processing...')
    for idx, match in progress_bar:
        # Set progress description
        progress_bar.set_description(desc=f'Processing... {idx+1}/{n_matches}')

        # Get match url
        match_url = url + match
        data = get_content(match_url, verbose=False)

        # Get match attributes, and player stats for the match
        if data['data']['type'] == 'match':
            game_mode = data['data']['attributes']['gameMode']
            map_name = data['data']['attributes']['mapName']
            game_duration = data['data']['attributes']['duration']
            shard_id = data['data']['attributes']['shardId']
            players = data['included']
            for player in players:
                if player['type'] == 'participant':
                    stats = player['attributes']['stats']
                    stats['matchId'] = match
                    stats['gameMode'] = game_mode
                    stats['mapName'] = map_name
                    stats['duration'] = game_duration
                    stats['platform'] = shard_id
                    pubg_stats.append(stats)
        
        time.sleep(1.5) # Slow down API request            
    return pd.DataFrame(pubg_stats)

def save_data_frame(df=None, filename=None):
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        print("Data Frame couldn't be saved: ", sys.exc_info()[0])
        raise

# matches = get_match_samples()
# print(matches.head())


# df = get_match_stats(matches)
# print(df.head())

# save_data_frame(df, 'pubg_stats.csv')