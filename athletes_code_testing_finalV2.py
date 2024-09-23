import csv
import pandas as pd
import os
import glob
from PIL import Image



# Function to check if the athlete's name is in the CSV file and return the DataFrame if found
def find_athlete_in_csv(athlete_name, csv_file):
    if not os.path.isfile(csv_file):
        return False # Return False if the file does not exist
    try:
        df = pd.read_csv(csv_file)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return False 
    if 'name' in df.columns:
        if athlete_name in df['name'].values:
            return df
    return False
    


# Define the CSV file and output HTML file
csv_file = "meets/37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.csv"
output_file = "html_temp_testing.html"
image_folder = "images/AthleteImages/"

try:
    # Open the CSV file and read the data
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

    # print(f"Number of rows in CSV: {len(data)}")
    # if len(data) > 6:  # Ensure there are enough rows to print
    #     for i in range(4, 6):  # Print 5th and 6th row
    #         print(f"Row {i}: {data[i]}")
    # else:
    #     for i, row in enumerate(data):
    #         print(f"Row {i}: {row}")

    # Debugging: Print number of rows and the content of the CSV


    print(f"Number of rows in CSV: {len(data)}")
    for i, row in enumerate(data[27:29]):
        print(f"Row {i}: {row}")

    # print(f"Number of rows in CSV: {len(data)}")
    # if len(data) > 6:  # Ensure there are enough rows to print
    #     #prints out 2
    #     for i in range(4, 6):
    
    # Check if we have enough rows in the CSV
    if len(data) < 7:  # Ensure there are at least 4 rows (header + meet info + athletes)
        raise ValueError("CSV file doesn't contain enough data.")

    # Extract general data from the CSV
    meet_name = data[0][0]  # Assuming first row is the meet name
    meet_date = data[1][0]  # Meet Date (second row)
    team_results_link = data[2][0]  # Team Results Link (third row)
    overall_team_results = data[3][0]  # Overall Team Results (fourth row)


    # Prepare athlete rows
    athlete_rows = ''



#Note: the feedback function is at the top ^

#make sure to end the previous debugging sessions that might mess up what is compiled



    for row in data[27:29]:  # Start from the fifth row for athletes
        # place, grade, name, time, team, picture
        if len(row) >= 5:  # Ensure there are enough columns
            athlete_place = row[0]  # Athlete Place
            athlete_name = row[2]
            athlete_grade = row[1]  # Athlete grade
           
           #Athlete Image URL
            athlete_imageURL = row[7]  # Athlete Image URL
            timing = row[4]  # Athlete Feedback


            #section for athlete_feedback
            # Directory containing the CSV files
            csv_mensdirectory = 'athletes/mens_team'
            csv_womensdirectory = 'athletes/womens_team'

            # Athlete name to search for
            #CHECK FOR DEBUG DO NOT FORGET
            #athlete_name = row[7]

            # Collect names of all CSV files in the directory
            csv_files = [f for f in os.listdir(csv_mensdirectory) if f.endswith('.csv')]
            csv_files1 = [f for f in os.listdir(csv_womensdirectory) if f.endswith('.csv')]
            

            # Loop through each CSV file and check for the athlete's name
            for csv_file in csv_files:
                csv_file_path = os.path.join(csv_mensdirectory, csv_file)
                #this is if it is found
                if find_athlete_in_csv(athlete_name, csv_file_path):
                    #print(f"Athlete {athlete_name} found in {csv_file}")
                    with open(csv_file, newline='', encoding='utf-8') as fileFeedback:
                        readerFeedback = csv.reader(fileFeedback)
                        dataFeedback = list(reader)
                        #COME BACK INCOMPLETE
                        break
                else:
                    #for this part I finished it it should work but I need to see what the dataset looks like 
                    #you will need to debug let me add breakpoints first
                    #print(f"Athlete {athlete_name} not found in {csv_file}")
                    athlete_feedback = ""
        
            #csv_dir = 'athletes/mens_team'

            #imageFill = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
            imageFill = glob.glob(os.path.join(image_folder,"*.jpg"))

            for csv_idk in imageFill:
                #csv_file_path1 = os.path.join(image_folder, csv_idk)
                csv_file_path1 = "{}{}".format(image_folder,str(csv_idk))
                if find_athlete_in_csv(athlete_imageURL, csv_file_path1):
                    image = Image.open(csv_file_path1)
                    athlete_image = image
                    #with open(csv_idk, newline='', encoding='utf-8') as fileFeedback1:
                     #   readerFeedback1 = csv.reader(fileFeedback1)
                      #  dataFeedback = list(reader)
                       # #COME BACK INCOMPLETE
                    break
                else:
                    athlete_image = athlete_imageURL




#            df_images = pd.read_csv(image_folder)
            
        # Check if the image file exists
 #           if os.path.isfile(athlete_image_path):
  #              athlete_image = athlete_image_path  # Use the full path to the image
   #         else:
    #            athlete_image = "default_image.jpg"

     #       athlete_image_filename = row[7]  # For example: '21198004.jpg'
      #      athlete_image_path = os.path.join(image_folder, athlete_image_filename)

            # Check if the image file exists
       #     if os.path.isfile(athlete_image_path):
        #        athlete_image = athlete_image_filename  # Use just the filename for HTML
         #   else:
          #      athlete_image = "default_image.jpg"
            


            
            
            
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
                    <th>Team</th>
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
    i+=1

except ValueError as ve:
   print(f"ValueError: {ve}")
except IndexError as ie:
    print(f"IndexError: {ie}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
