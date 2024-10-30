import datetime
import requests

def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    
    if (end_time_s < start_time_s):
        raise ValueError('The end of the range has to come strictly after its start.')
    # calculate the single interval
    # below code achieves the same result: single duration of each interval
    d = ((end_time_s - start_time_s).total_seconds() - gap_between_intervals_s * (number_of_intervals - 1)) / number_of_intervals
    # d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)

    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                for i in range(number_of_intervals)]

    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            # bug fixing: only overlapping exists, below min/max range satisfy
            #if start2<=end1 and end2>=start1:
            low = max(start1, start2)
            high = min(end1, end2)
            if low<high:
                overlap_time.append((low, high))
    return overlap_time

    
def iss_passes():
    key = '33Q884-HFUV8K-SCS3LG-55CU'
    url = f'https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/41.702/-76.014/0/2/300/&apiKey={key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        pass_times = [
            (
            datetime.datetime.fromtimestamp(info["startUTC"]).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.datetime.fromtimestamp(info["endUTC"]).strftime("%Y-%m-%d %H:%M:%S")
            )
            for info in data.get("passes", [])
        ]
        return pass_times
    else:
        raise Exception(f"Resquest failed: {response.status_code}")



if __name__ == "__main__":
    # large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    # short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    # print(compute_overlap_time(large, short))
    
    pass_times = iss_passes()
    print(pass_times)
    
    