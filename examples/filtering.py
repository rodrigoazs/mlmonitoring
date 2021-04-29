from mlmonitoring import MLmonitoring


def perform_filtering():
    # monitoring
    monitor = MLmonitoring() \
        .set_connection('http://localhost:8000') \
        .set_project('breast_cancer') \

    print('Entire table')
    print(monitor.view('average_recall'))
    
    print('Table filtered')
    print(monitor.filter(
        'average_recall',
        recall__gt=0.98
    ))


if __name__ == "__main__":
    perform_filtering()
