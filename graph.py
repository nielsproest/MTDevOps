import json, datetime
import matplotlib.pyplot as plt
import numpy as np
import random, json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

data = {}
with open("out.json") as f:
	data = json.load(f)

def issues_of_day():
	res = {
		"HIGH": {
			"HIGH": [],
			"MEDIUM": [],
			"LOW": [],
		},
		"MEDIUM": {
			"HIGH": [],
			"MEDIUM": [],
			"LOW": [],
		},
		"LOW": {
			"HIGH": [],
			"MEDIUM": [],
			"LOW": [],
		},
	}

	for i in data["2023-6-26"]["results"]:
		res[i["issue_severity"]][i["issue_confidence"]].append(i)

	print(json.dumps(res["MEDIUM"]["LOW"], indent="\t"))

def issues_pr_weekday():
	days = [[] for _ in range(7)]
	for i in data:
		dt = datetime.datetime.strptime(i, "%Y-%m-%d")
		day_of_week = dt.weekday()
		days[day_of_week].append(len(data[i]["results"]))

	days = [sum(i) / len(i) for i in days]

	xpoints = [i for i in range(7)]
	ypoints = days
	plt.plot(xpoints, ypoints)
	plt.title("Average number of issues in a week (in 2023)")
	plt.xlabel("Day of week")
	plt.ylabel("Number of detected issues")
	#plt.show()
	plt.savefig("issues_pr_week_day.png")

def issues_pr_weekday_avg():
	pass

# Number of critical/high/medium/low pr day
def issues_pr_weekday_by_criticality():
	days = [{"LOW": 0, "MEDIUM": 0, "HIGH": 0} for _ in range(7)]
	for i in data:
		dt = datetime.datetime.strptime(i, "%Y-%m-%d")
		day_of_week = dt.weekday()
		for j in data[i]["results"]:
			_severity = j["issue_severity"]
			days[day_of_week][_severity] += 1

	names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday", "Saturday"]
	means = {
		"LOW": [days[day_of_week]["LOW"] for day_of_week in range(7)],
		"MEDIUM": [days[day_of_week]["MEDIUM"] for day_of_week in range(7)],
		"HIGH": [days[day_of_week]["HIGH"] for day_of_week in range(7)]
	}

	x = np.arange(len(names))  # the label locations
	width = 0.25  # the width of the bars
	multiplier = 0

	fig, ax = plt.subplots(layout='constrained')

	for attribute, measurement in means.items():
		offset = width * multiplier
		rects = ax.bar(x + offset, measurement, width, label=attribute)
		ax.bar_label(rects, padding=3)
		multiplier += 1

	# Add some text for labels, title and custom x-axis tick labels, etc.
	plt.xlabel("Day of week")
	ax.set_ylabel('Number of issues')
	ax.set_title('Average number of issues in a week (in 2023)')
	ax.set_xticks(x + width, names)
	ax.legend(loc='upper left', ncols=3)
	plt.savefig("issues_pr_weekday_by_criticality.png")

# Number of critical/high/medium/low pr day
def issues_pr_weekday_by_criticality_avg():
	days = [{"LOW": 0, "MEDIUM": 0, "HIGH": 0} for _ in range(7)]
	avg = [0 for _ in range(7)]
	for i in data:
		dt = datetime.datetime.strptime(i, "%Y-%m-%d")
		day_of_week = dt.weekday()
		for j in data[i]["results"]:
			_severity = j["issue_severity"]
			days[day_of_week][_severity] += 1
			avg[day_of_week] += 1

	names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday", "Saturday"]
	means = {
		"LOW": [days[day_of_week]["LOW"]/avg[day_of_week] for day_of_week in range(7)],
		"MEDIUM": [days[day_of_week]["MEDIUM"]/avg[day_of_week] for day_of_week in range(7)],
		"HIGH": [days[day_of_week]["HIGH"]/avg[day_of_week] for day_of_week in range(7)]
	}

	x = np.arange(len(names))  # the label locations
	width = 0.25  # the width of the bars
	multiplier = 0

	fig, ax = plt.subplots(layout='constrained')

	for attribute, measurement in means.items():
		offset = width * multiplier
		rects = ax.bar(x + offset, measurement, width, label=attribute)
		ax.bar_label(rects, padding=3)
		multiplier += 1

	# Add some text for labels, title and custom x-axis tick labels, etc.
	plt.xlabel("Day of week")
	ax.set_ylabel('Number of issues')
	ax.set_title('Average number of issues in a week (in 2023)')
	ax.set_xticks(x + width, names)
	ax.legend(loc='upper left', ncols=3)
	plt.savefig("issues_pr_weekday_by_criticality_avg.png")

# Number of critical/high/medium/low pr day
def issues_pr_weekday_by_criticality_avg_high():
	days = [{"LOW": 0, "MEDIUM": 0, "HIGH": 0} for _ in range(7)]
	avg = [0 for _ in range(7)]
	for i in data:
		dt = datetime.datetime.strptime(i, "%Y-%m-%d")
		day_of_week = dt.weekday()
		for j in data[i]["results"]:
			_severity = j["issue_severity"]
			days[day_of_week][_severity] += 1
			avg[day_of_week] += 1

	names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday", "Saturday"]
	means = [days[day_of_week]["HIGH"]/avg[day_of_week] for day_of_week in range(7)]

	xpoints = names
	ypoints = means
	plt.plot(xpoints, ypoints)
	plt.title("Average number of high severity issues pr week (in 2023)")
	plt.xlabel("Day of week")
	plt.ylabel("Number of detected high severity issues")
	plt.subplots_adjust(left=0.15)
	#plt.show()
	plt.savefig("issues_pr_weekday_by_criticality_avg_high.png")


# Number of issues by month (sum and individual)
def issues_by_month():
	pass

# Number of issues by year? (or more)
def issues_graph_year():
	pass

from collections import defaultdict
def issues_over_time():
	issue_count_by_date_severity = defaultdict(lambda: defaultdict(int))

	for date in data:
		for result in data[date]["results"]:
			issue_severity = result["issue_severity"]
			if issue_severity == "LOW":
				continue
			dt = datetime.datetime.strptime(date, "%Y-%m-%d")
			issue_count_by_date_severity[dt][issue_severity] += 1

	unique_severities = set()
	for date_data in issue_count_by_date_severity.values():
		unique_severities.update(date_data.keys())

	sorted_dates = sorted(issue_count_by_date_severity.keys())

	plt.figure(figsize=(10, 6))

	for severity in unique_severities:
		x = []
		y = []
		for date in sorted_dates:
			x.append(date)
			y.append(issue_count_by_date_severity[date][severity])
		plt.plot(x, y, label=severity)

	plt.xlabel("Date")
	plt.ylabel("Number of Issues")
	plt.title("Progression of Issues by Date and Severity Without Low Severity")
	plt.xticks(rotation=45)
	plt.legend()
	plt.tight_layout()

	#plt.show()
	plt.savefig("issues_over_time_no_low.png")

def issues_survival():
	issues = {}

	def exists(k):
		for i in issues:
			if similar(i,k) >= 0.6:
				return i
		return False

	for date in data:
		print(date)
		for results in data[date]["results"]:
			if not results['issue_severity'] in ["HIGH", "MEDIUM"]:
				continue

			k = f"{results['filename']}@{results['code']}"
			r = exists(k)
			if r == False:
				issues[k] = [date]
			else:
				issues[r].append(date)

	with open("issues_survival.json", "w") as f:
		json.dump(issues, f, indent="\t")

def issues_survival_graph():
	s = {}
	with open("issues_survival.json") as f:
		s = json.load(f)

	issue_dates = defaultdict(list)
	for issue, dates in s.items():
		for date in dates:
			issue_dates[issue].append(datetime.datetime.strptime(date, "%Y-%m-%d"))

	issue_persistence = {}
	for issue, dates in issue_dates.items():
		min_date = min(dates)
		max_date = max(dates)
		persistence = max_date - min_date
		issue_persistence[issue] = persistence

	sorted_issues = sorted(issue_persistence.keys(), key=lambda issue: min(issue_dates[issue]))

	issue_names = []
	persistence_durations = []
	for issue in sorted_issues:
		issue_names.append(issue[-14:])
		persistence_durations.append(issue_persistence[issue].days)

	# Plotting
	plt.figure(figsize=(10, 6))
	plt.barh(issue_names, persistence_durations, color='skyblue')
	plt.xlabel("Persistence Duration (days)")
	plt.ylabel("Issues")
	plt.title("Issues and Their Persistence Duration")
	plt.tight_layout()

	plt.show()
	#plt.savefig("issues_survival.png")

def issues_survival_text():
	s = {}
	with open("issues_survival.json") as f:
		s = json.load(f)

	issue_dates = defaultdict(list)
	issue_info = {}
	for issue, dates in s.items():
		for date in dates:
			issue_dates[issue].append(datetime.datetime.strptime(date, "%Y-%m-%d"))
			found = False
			for _date in data:
				for res in data[_date]["results"]:
					if res["code"] in issue:
						issue_info[issue] = [
							res["issue_text"],
							res["issue_severity"],
							res["issue_confidence"],
						]
						found = True
						break
				if found:
					break

	issue_persistence = {}
	for issue, dates in issue_dates.items():
		min_date = min(dates)
		max_date = max(dates)
		persistence = max_date - min_date
		issue_persistence[issue] = {
			"first_appeared_date": min_date,
			"last_seen_date": max_date,
			"survival_in_days": persistence.days
		}

	sorted_issues = sorted(issue_persistence.keys(), key=lambda issue: min(issue_dates[issue]))

	output_filename = "issue_survival_details.txt"
	with open(output_filename, "w") as f:
		for issue in sorted_issues:
			details = issue_persistence[issue]
			f.write(f"Issue: {issue}")
			dat = details['first_appeared_date'].strftime('%Y-%m-%d')
			t,ta,tb = issue_info[issue]
			f.write(f"Issue Text: {t}\n")
			f.write(f"Issue Severity: {ta}\n")
			f.write(f"Issue Confidence: {tb}\n")
			f.write(f"First appeared date: {dat}\n")
			f.write(f"Last seen date: {details['last_seen_date'].strftime('%Y-%m-%d')}\n")
			f.write(f"Survival in days: {details['survival_in_days']}\n")
			f.write("\n")


if __name__ == "__main__":
	issues_of_day()
	#issues_pr_weekday()
	#issues_pr_weekday_by_criticality()
	#issues_pr_weekday_by_criticality_avg()
	#issues_pr_weekday_by_criticality_avg_high()
	#issues_survival()
	#issues_over_time()
	#issues_survival_graph()
	#issues_survival_text()
