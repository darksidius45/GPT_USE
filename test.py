import openpyxl
import json
import subprocess
import tempfile
import os
# from config import promt
promt = (
    "Definition of AV Integrations: A Comprehensive Overview\n\n"
    "AV (Audio-Visual) integrations refer to the seamless incorporation of audio, video, and control systems into various environments, ranging from small meeting rooms to large-scale conference spaces, training facilities, and beyond. These integrations are designed to enhance communication, collaboration, and user experience by combining hardware, software, and network technologies into a unified, user-friendly ecosystem. Below is a detailed breakdown of AV integrations at all levels, from workshops to meeting rooms:\n\n"
    "1. Core Components of AV Integrations\n"
    "AV integrations typically involve the following elements:\n\n"
    "Audio Systems: Microphones, speakers, amplifiers, and sound processors for clear audio delivery.\n\n"
    "Video Systems: Displays (e.g., monitors, projectors, LED walls), cameras, and video processors for high-quality visuals.\n\n"
    "Control Systems: Interfaces (e.g., touch panels, remotes, apps) to manage AV equipment and room functions.\n\n"
    "Connectivity: Cabling, wireless solutions, and network infrastructure to enable communication between devices.\n\n"
    "Software: Collaboration tools, video conferencing platforms, and room scheduling systems.\n\n"
    "Automation: Integration with IoT (Internet of Things) for smart room controls (e.g., lighting, blinds, HVAC).\n\n"
    "2. Levels of AV Integrations\n"
    "a. Small-Scale Integrations (Workshops and Huddle Rooms)\n"
    "Purpose: Facilitate quick, informal meetings or brainstorming sessions.\n\n"
    "Key Features:\n\n"
    "Compact audio systems (e.g., tabletop microphones, soundbars).\n\n"
    "Small displays or interactive whiteboards.\n\n"
    "Basic video conferencing setups (e.g., webcams, all-in-one systems like Microsoft Teams Rooms or Zoom Rooms).\n\n"
    "Simple control interfaces (e.g., touch panels or mobile apps).\n\n"
    "Examples: Huddle rooms, small training spaces, or creative workshops.\n\n"
    "b. Medium-Scale Integrations (Meeting Rooms and Classrooms)\n"
    "Purpose: Support structured meetings, presentations, and collaborative learning.\n\n"
    "Key Features:\n\n"
    "Advanced audio systems with beamforming microphones for voice clarity.\n\n"
    "Larger displays or projection systems for presentations.\n\n"
    "Integrated video conferencing with PTZ (pan-tilt-zoom) cameras.\n\n"
    "Room scheduling systems and occupancy sensors.\n\n"
    "Interactive displays or digital whiteboards for collaboration.\n\n"
    "Examples: Corporate meeting rooms, university classrooms, or training centers.\n\n"
    "c. Large-Scale Integrations (Conference Rooms and Auditoriums)\n"
    "Purpose: Host large groups for presentations, conferences, or events.\n\n"
    "Key Features:\n\n"
    "High-quality audio systems with ceiling microphones and line arrays.\n\n"
    "Large-format displays, video walls, or multiple projectors.\n\n"
    "Advanced video conferencing with multiple cameras and streaming capabilities.\n\n"
    "Centralized control systems for managing complex setups.\n\n"
    "Integration with event management and live streaming platforms.\n\n"
    "Examples: Boardrooms, lecture halls, or event spaces.\n\n"
    "d. Enterprise-Wide Integrations (Multi-Room and Campus-Wide Systems)\n"
    "Purpose: Provide consistent AV experiences across multiple rooms or locations.\n\n"
    "Key Features:\n\n"
    "Unified control systems (e.g., Crestron, Extron) for managing multiple rooms.\n\n"
    "Cloud-based management platforms for monitoring and maintenance.\n\n"
    "Standardized hardware and software across all spaces.\n\n"
    "Integration with IT infrastructure for secure, scalable solutions.\n\n"
    "Remote monitoring and troubleshooting capabilities.\n\n"
    "Examples: Corporate campuses, educational institutions, or healthcare facilities.\n\n"
    "3. Benefits of AV Integrations\n"
    "Enhanced Collaboration: Enables seamless communication and content sharing.\n\n"
    "Improved User Experience: Simplifies operation with intuitive controls.\n\n"
    "Scalability: Adapts to the needs of small teams or large organizations.\n\n"
    "Cost Efficiency: Reduces long-term costs through centralized management.\n\n"
    "Future-Proofing: Supports emerging technologies and upgrades.\n\n"
    "4. Key Considerations for AV Integrations\n"
    "User Needs: Tailor solutions to the specific requirements of the space and users.\n\n"
    "Interoperability: Ensure compatibility between different devices and platforms.\n\n"
    "Network Infrastructure: Plan for sufficient bandwidth and security.\n\n"
    "Acoustics and Lighting: Optimize room design for audio and video quality.\n\n"
    "Support and Maintenance: Provide training and ongoing technical support.\n\n"
    "5. Emerging Trends in AV Integrations\n"
    "AI and Machine Learning: For intelligent automation and analytics.\n\n"
    "Immersive Technologies: AR/VR for enhanced collaboration and training.\n\n"
    "Wireless Solutions: For flexible, cable-free setups.\n\n"
    "Sustainability: Energy-efficient systems and eco-friendly materials.\n\n"
    "In summary, AV integrations are a critical component of modern workspaces, educational environments, and event venues. By combining cutting-edge technology with thoughtful design, AV integrations empower users to communicate, collaborate, and create more effectively."
)

def gemini_flash(text):
    # Create a temporary file to store the JSON data
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json_data = {
            "contents": [{"role": "user", "parts": [{"text": text}]}]
        }
        json.dump(json_data, temp_file)
        temp_file.flush()  # Ensure the data is written

        # Get the name of the temporary file
        temp_file_name = temp_file.name

    try:
        # Simplified curl command using the temporary file
        curl_command = [
            "curl",
            "https://api.proxyapi.ru/google/v1/models/gemini-1.5-flash:generateContent",
            "-H", "Content-Type: application/json",
            "-H", "Authorization: Bearer sk-UmoxJZ8wJm1DEmcSrwP3Iu9Bk4TGZJ0h",
            "-d", f"@{temp_file_name}"  # Use the temp file
        ]

        result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            response = json.loads(result.stdout)
            text_response = response['candidates'][0]['content']['parts'][0]['text']
            print(text_response)
            return text_response
        else:
            print("Error executing curl command:", result.stderr)
            return None
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)




df = openpyxl.load_workbook("out.xlsx")
sheet = df.active
for row in sheet.iter_rows(min_row=3):
    name = row[0].value
    site = row[1].value
    phone_number = row[2].value
    adress = row[3].value
    categories = row[4].value
    about_little = row[5].value
    site_text = row[6].value
    if site_text != "":
        site_text_short = gemini_flash(f"tell me about this company categroies:{categories} , about them{about_little}, their site:{site_text}")
        answer = gemini_flash(f"tell me if this company is connected with av integrations(i need 1 world yes or no in the begging then, distributor” или “integrator” или “manufacturer, and only then why) company info - categroies:{categories} , about them{about_little}, their site:{site_text}. AV integrations: {promt}")
        sheet.append([name, site, phone_number, adress, categories, about_little, site_text_short, answer]) 
    df.save("out.xlsx")