import csv
import sys

if len(sys.argv) != 2:
	print("Use: python read_csv.py file.csv")
	sys.exit(1)

card_ids = set()

with open(sys.argv[1], newline='', encoding='utf-8') as f:
	reader = csv.DictReader(f, delimiter=';')

	for row in reader:
		card_id = row["old_card_token"]

		if card_id in card_ids:
			print(row)
			continue

		card_ids.add(card_id)
