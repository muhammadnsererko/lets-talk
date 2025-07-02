import json
import os
from collections import Counter, defaultdict

ANALYTICS_PATH = os.path.join(os.path.dirname(__file__), 'analytics_data.json')

def load_analytics():
    if not os.path.exists(ANALYTICS_PATH):
        print('No analytics_data.json found.')
        return []
    with open(ANALYTICS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f'Error loading analytics_data.json: {e}')
            return []
    # Flatten events if stored as dict of lists
    if isinstance(data, dict):
        events = []
        for user_events in data.values():
            if isinstance(user_events, list):
                events.extend(user_events)
        return events
    elif isinstance(data, list):
        return data
    return []

def analyze_failures(events):
    failure_events = [e for e in events if e.get('event') in ('test_failure', 'api_error')]
    error_counter = Counter()
    test_counter = Counter()
    error_details = defaultdict(list)
    for e in failure_events:
        error = e.get('details', {}).get('error', 'Unknown')
        test = e.get('details', {}).get('test', 'Unknown')
        error_counter[error] += 1
        test_counter[test] += 1
        error_details[error].append(test)
    print(f"Total failures: {len(failure_events)}")
    print("Most common errors:")
    for err, count in error_counter.most_common(10):
        print(f"  {err}: {count} times (tests: {set(error_details[err])})")
    print("Most failing tests:")
    for test, count in test_counter.most_common(10):
        print(f"  {test}: {count} failures")

def main():
    events = load_analytics()
    if not events:
        print('No events to analyze.')
        return
    analyze_failures(events)

if __name__ == '__main__':
    main()