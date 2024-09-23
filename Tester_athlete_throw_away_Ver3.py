import csv
import os

# Define feedback for each athlete
athlete_feedback_dict = {
    "Beckett Crooks": "Great performance!",
    "Alex Doneth": "Strong finish!",
    # Add more athletes and their feedback as needed
    # I dont know if this is right (I think it's better than otherwise TAT)
}

# Function to check if the athlete's name is in the CSV file and return the DataFrame if found
def find_athlete_in_csv(athlete_name, csv_file):
    if not os.path.isfile(csv_file):
        return False  # Return False if the file does not exist
    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if athlete_name.lower() == row[2].lower():  # Assuming athlete name is in the third column
                    return True
    except (csv.Error):
        return False
    return False

# Define the CSV file and output HTML file
csv_file = "meets/37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.csv"
output_file = "html_temp_testing.html"
image_folder = "images/"

try:
    # Open the CSV file and read the data
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

    print(f"Number of rows in CSV: {len(data)}")

    # Check if we have enough rows in the CSV
    if len(data) < 7:  # Ensure there are enough rows
        raise ValueError("CSV file doesn't contain enough data.")

    # Extract general data from the CSV
    meet_name = data[0][0]  # Meet Name
    meet_date = data[1][0]  # Meet Date
    team_results_link = data[2][0]  # Team Results Link
    overall_team_results = data[3][0]  # Overall Team Results

    # Prepare athlete rows
    athlete_rows = ''

    for row in data[27:29]:  # Start from the fifth row for athletes
        # place, grade, name, time, team, picture
        if len(row) >= 5:  # Ensure there are enough columns
            athlete_place = row[0]  # Athlete Place
            athlete_name = row[2]
            athlete_grade = row[1]  # Athlete grade
            athlete_image = row[7]  # Athlete Image URL
            timing = row[4]  # Athlete Feedback
            athlete_image_filename = row[5]

            # Construct the full path to the image
            athlete_image_path = os.path.join(image_folder, athlete_image_filename)

            # Check if the image file exists
            if os.path.isfile(athlete_image_path):
                athlete_image = athlete_image_filename  # Use just the filename for HTML
            else:
                athlete_image = "default_image.jpg"  # Fallback if not found

            # Get feedback from the predefined dictionary
            athlete_feedback = athlete_feedback_dict.get(athlete_name, "")  # Default to empty string if not found

            athlete_rows += f'''
            <tr>
                <td>{athlete_place}</td>
                <td>{athlete_name}</td>
                <td>{timing}</td>
                <td><img src="{athlete_image}" alt="{athlete_name}" /></td>
                <td>{athlete_feedback}</td>
            </tr>
            '''

    # Combine template with data
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style.css">
    <title>{meet_name} Country Meet</title>
</head>
<body>
    <header>
        <h1>{meet_name}</h1>
        <h2>{meet_date}</h2>
    </header>
    <section id="team-results">
        <h2>Overall Team Results</h2>
        <p><a href="{team_results_link}">Team results are available here.</a></p>
        <p>{overall_team_results}</p>
    </section>
    <section id="athlete-results">
        <h2>Athlete Results</h2>
        <table id="athlete-table">
            <thead>
                <tr>
                    <th>Place</th>
                    <th>Name</th>
                    <th>Timing</th>
                    <th>Image</th>
                    <th>Feedback</th>
                </tr>
            </thead>
            <tbody>
                {athlete_rows}
            </tbody>
        </table>
    </section>
</body>
</html>'''

    # Write the HTML content to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML content written to {output_file}")

except ValueError as ve:
    print(f"ValueError: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
