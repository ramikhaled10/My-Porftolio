import os
import sys

# Ensure UTF-8 output compatibility across Windows terminals
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from slugify import slugify
from app import create_app
from app.extensions import db
from app.models import (
    User, Project, Skill, SkillCategory, Education,
    Certification, SiteSetting
)

app = create_app('development')



def seed_database():
    with app.app_context():
        print("🌱 Starting database seeding...")
        db.create_all()

        # 1. Admin User
        admin_username = os.getenv('ADMIN_USERNAME', 'rami')
        admin_email = os.getenv('ADMIN_EMAIL', 'rami.khaled@example.dz')
        admin_password = os.getenv('ADMIN_PASSWORD', 'AdminRami2026!')

        user = User.query.filter_by(username=admin_username).first()
        if not user:
            user = User(
                username=admin_username,
                email=admin_email,
                is_admin=True
            )
            user.set_password(admin_password)
            db.session.add(user)
            print(f"✓ Created admin user: {admin_username} ({admin_email})")
        else:
            print(f"✓ Admin user '{admin_username}' already exists.")

        # 2. Site Settings
        settings_data = [
            ('hero_tagline', 'Engineer in progress. Developer by curiosity. Builder by ambition.', 'Main hero tagline'),
            ('hero_bio', "First-year engineering student at École Nationale Polytechnique d'Alger (ENP). Passionate about turning algorithmic problem-solving and clean code into real software, with an active focus on Python backend architecture, Flutter mobile development, and applied AI systems.", 'Hero introductory bio'),
            ('status_text', 'First-year Engineering Student @ ENP Algiers', 'Current status badge text'),
            ('github_url', 'https://github.com/ramikhaled', 'GitHub Profile URL'),
            ('linkedin_url', 'https://linkedin.com/in/rami-khaled', 'LinkedIn Profile URL'),
            ('contact_email', 'rami.khaled@example.dz', 'Primary contact email')
        ]
        for key, val, desc in settings_data:
            if not SiteSetting.query.filter_by(key=key).first():
                db.session.add(SiteSetting(key=key, value=val, description=desc))
        print("✓ Seeded site settings.")

        # 3. Education Milestones
        if Education.query.count() == 0:
            education_data = [
                Education(
                    institution="École Nationale Polytechnique d'Alger (ENP)",
                    degree="First-Year Engineering Student (Cycle Préparatoire)",
                    location="Algiers, Algeria",
                    start_year="2026",
                    end_year="Present",
                    grade="First-Year Engineering",
                    highlights="Intensive Engineering Mathematics | Advanced Physics | Algorithmic Thinking | Applied Engineering Sciences",
                    description="Admitted to Algeria's premier engineering institute following high academic distinction in the national Baccalaureate. Currently developing deep foundations in calculus, engineering physics, mechanics, and algorithmic problem solving.",
                    order_num=1
                ),
                Education(
                    institution="High School (Lycée Souk El Tennine)",
                    degree="Algerian Baccalaureate — Technique Mathématiques (Génie Électrique)",
                    location="Souk El Tennine, Béjaïa, Algeria",
                    start_year="2023",
                    end_year="2026",
                    grade="17.80 / 20 (Mention Très Bien)",
                    highlights="Mathematics: 18 / 20 | Physics: 19.5 / 20 | Electrical Engineering: 19.5 / 20",
                    description="Focused on electrical engineering fundamentals, digital logic, circuit analysis, and advanced mathematics. Achieved near-perfect scores across core technical subjects, graduating at the top academic tier.",
                    order_num=2
                ),
                Education(
                    institution="Middle School (CEM Souk El Tennine)",
                    degree="Brevet d'Enseignement Moyen (BEM)",
                    location="Souk El Tennine, Béjaïa, Algeria",
                    start_year="2019",
                    end_year="2023",
                    grade="17.43 / 20 (Mention Très Bien)",
                    highlights="Mathematics: 20 / 20 | Natural Sciences: 19 / 20 | Physics: 18 / 20",
                    description="Demonstrated early passion for quantitative sciences with a perfect 20/20 in mathematics and exceptional distinction in natural sciences and physics.",
                    order_num=3
                ),
                Education(
                    institution="Primary School (École Primaire Souk El Tennine)",
                    degree="Primary Education Completion (6ème)",
                    location="Souk El Tennine, Béjaïa, Algeria",
                    start_year="2014",
                    end_year="2019",
                    grade="9.30 / 10",
                    highlights="Foundational Academic Distinction in Mathematics & Languages",
                    description="Early education completed in Souk El Tennine, establishing early reading habits, disciplined curiosity, and affinity for mathematics.",
                    order_num=4
                )
            ]
            db.session.add_all(education_data)
            print("✓ Seeded authentic academic milestones.")

        # 4. Skill Categories and Skills
        if SkillCategory.query.count() == 0:
            cat_prog = SkillCategory(name="Programming Languages", icon="code-2", order_num=1)
            cat_back = SkillCategory(name="Backend & Databases", icon="database", order_num=2)
            cat_mobile = SkillCategory(name="Mobile & UI", icon="smartphone", order_num=3)
            cat_eco = SkillCategory(name="Python Ecosystem", icon="cpu", order_num=4)
            cat_eng = SkillCategory(name="Core Engineering Concepts", icon="layers", order_num=5)

            db.session.add_all([cat_prog, cat_back, cat_mobile, cat_eco, cat_eng])
            db.session.flush()

            skills_data = [
                # Programming
                Skill(name="Python", category_id=cat_prog.id, level="Comfortable", description="Primary language for backend, automation scripts, algorithms, and data analysis.", order_num=1),
                Skill(name="SQL", category_id=cat_prog.id, level="Familiar", description="Relational querying, schema design, filtering, joins, and indexing fundamentals.", order_num=2),
                Skill(name="HTML5 & CSS3", category_id=cat_prog.id, level="Comfortable", description="Semantic layout structures, responsive styling, flexbox, CSS grid, and modern web design.", order_num=3),
                Skill(name="JavaScript", category_id=cat_prog.id, level="Familiar", description="Client-side DOM manipulation, asynchronous fetch APIs, and interactive UI behavior.", order_num=4),
                Skill(name="Dart", category_id=cat_prog.id, level="Developing", description="Object-oriented programming language powering Flutter applications.", order_num=5),

                # Backend
                Skill(name="Flask", category_id=cat_back.id, level="Familiar", description="Modular backend routing with Blueprints, Jinja templating, and request handling.", order_num=1),
                Skill(name="PostgreSQL", category_id=cat_back.id, level="Familiar", description="Robust relational database system used for production data storage and migrations.", order_num=2),
                Skill(name="SQLAlchemy", category_id=cat_back.id, level="Familiar", description="Python ORM for declarative model definition, relationships, and transaction management.", order_num=3),
                Skill(name="RESTful APIs", category_id=cat_back.id, level="Familiar", description="Endpoint design, JSON serialization, HTTP status conventions, and authentication.", order_num=4),

                # Mobile
                Skill(name="Flutter", category_id=cat_mobile.id, level="Developing", description="Cross-platform UI framework for Android & iOS; currently building mobile layouts.", order_num=1),
                Skill(name="State Management", category_id=cat_mobile.id, level="Developing", description="Exploring clean state handling and widget lifecycle in mobile applications.", order_num=2),

                # Python Ecosystem
                Skill(name="Requests", category_id=cat_eco.id, level="Comfortable", description="HTTP communication, consuming REST APIs, headers, and authentication handling.", order_num=1),
                Skill(name="BeautifulSoup", category_id=cat_eco.id, level="Comfortable", description="HTML parsing, web data scraping, selector queries, and data extraction pipelines.", order_num=2),
                Skill(name="Selenium", category_id=cat_eco.id, level="Familiar", description="Browser automation, dynamic page navigation, wait conditions, and bot workflows.", order_num=3),
                Skill(name="Tkinter", category_id=cat_eco.id, level="Familiar", description="Desktop GUI engineering, event loops, layout managers, and canvas rendering.", order_num=4),
                Skill(name="Pandas", category_id=cat_eco.id, level="Developing", description="DataFrame manipulation, data cleaning, filtering, and aggregation.", order_num=5),
                Skill(name="NumPy", category_id=cat_eco.id, level="Developing", description="Numerical computing, multi-dimensional array operations, and vector calculations.", order_num=6),
                Skill(name="Matplotlib", category_id=cat_eco.id, level="Developing", description="Data visualization, plot customization, multi-axis charting, and trend plotting.", order_num=7),

                # Core Engineering
                Skill(name="Object-Oriented Programming (OOP)", category_id=cat_eng.id, level="Comfortable", description="Encapsulation, inheritance, polymorphism, and class-based modular software design.", order_num=1),
                Skill(name="API Architecture", category_id=cat_eng.id, level="Familiar", description="Designing structured client-server contracts and consuming public web services.", order_num=2),
                Skill(name="Database Design", category_id=cat_eng.id, level="Familiar", description="Relational modeling, foreign keys, normalization, and integrity constraints.", order_num=3),
                Skill(name="Web Automation", category_id=cat_eng.id, level="Familiar", description="Automating repetitive browser tasks, schedule execution, and parsing output.", order_num=4),
                Skill(name="Algorithmic Thinking", category_id=cat_eng.id, level="Comfortable", description="Breakdown of complex problems into clear mathematical and procedural steps.", order_num=5)
            ]
            db.session.add_all(skills_data)
            print("✓ Seeded skill categories and realistic skill proficiencies.")

        # 5. Certifications
        if Certification.query.count() == 0:
            cert_data = [
                Certification(
                    title="100 Days of Code: The Complete Python Pro Bootcamp",
                    issuer="Udemy / Dr. Angela Yu",
                    issue_date="Completed",
                    description="Comprehensive project-driven curriculum covering Python fundamentals, OOP, GUI development (Tkinter/Turtle), Web Scraping (BeautifulSoup/Selenium), Web Development (Flask), APIs, and intro Data Science (Pandas/NumPy/Matplotlib). Built over 20+ distinct hands-on software projects.",
                    credential_url=None,
                    skills_covered="Python, Flask, OOP, Tkinter, Selenium, BeautifulSoup, REST APIs, Pandas, SQL",
                    order_num=1
                ),
                Certification(
                    title="Flutter & Dart Mobile Development",
                    issuer="Coursera / IBM",
                    issue_date="Active / In Progress",
                    description="Professional coursework focused on Dart programming syntax, object orientation, Flutter widget trees, cross-platform mobile layouts, and state management fundamentals.",
                    credential_url=None,
                    skills_covered="Flutter, Dart, Mobile UI Design, Widget Lifecycle, Cross-Platform Development",
                    order_num=2
                )
            ]
            db.session.add_all(cert_data)
            print("✓ Seeded authentic certifications.")

        # 6. Projects (Honest, realistic learning and practical projects)
        if Project.query.count() == 0:
            projects_data = [
                Project(
                    title="Morse Code Audio & Text Converter",
                    slug="morse-code-converter",
                    summary="A bidirectional Python translation tool that converts raw alphanumeric text into standardized international Morse code and vice versa, featuring sound playback synthesis.",
                    description="This project was built to master dictionary data structures, bidirectional lookup mapping, string sanitization, and error-handling edge cases in Python. It converts alphanumeric characters to Morse code dots and dashes while handling spacing, punctuation, and frequency-based audio beeps.",
                    problem="Converting raw human text to Morse code requires addressing ambiguity in spacing between characters and words, handling non-Latin symbols gracefully, and providing immediate sensory feedback rather than just static text output.",
                    approach="Constructed an immutable bidirectional dictionary map. Built a parser that normalizes inputs, validates token streams against supported ITU specifications, and sequentially generates corresponding timing frequencies.",
                    key_features="• Full bidirectional translation (Text ⇄ Morse Code)\n• Audio synthesis for dot and dash duration intervals\n• Resilient error handling for unsupported characters\n• Clean terminal interface with instant CLI execution",
                    key_learnings="Deepened my understanding of dictionary inverted lookups, string tokenization, audio timing synchronization in Python, and defensive input parsing.",
                    challenges="Ensuring precise timing differentiation between intra-character dot/dash pauses and word-level separation intervals.",
                    future_improvements="Add microphone audio input with FFT sound frequency recognition to decode incoming audio beeps in real time.",
                    category="Python",
                    technologies="Python, Audio Synthesis, Data Structures, CLI",
                    github_url=None,
                    demo_url=None,
                    featured=True,
                    published=True,
                    order_num=1
                ),
                Project(
                    title="Tkinter & Pillow Desktop Watermark App",
                    slug="tkinter-pillow-watermark-app",
                    summary="A desktop GUI utility built with Python Tkinter and Pillow (PIL) that allows users to batch-apply custom text or graphic watermarks to photos with opacity and positioning controls.",
                    description="Built to explore native desktop GUI development and image manipulation pipelines. Users can load single or batch images, customize text content, adjust RGBA alpha transparency, select anchor placements, and export processed imagery.",
                    problem="Protecting original photography and digital assets typically requires heavyweight commercial software. A lightweight, local offline tool solves this with zero dependencies on cloud uploads.",
                    approach="Integrated Tkinter's Canvas and FileDialog modules with Pillow's Image and ImageDraw libraries. Implemented real-time thumbnail previewing with non-destructive image compositing before file saving.",
                    key_features="• Load JPEG/PNG/WebP formats via native file picker\n• Real-time interactive visual preview canvas\n• Customizable text font, size, opacity slider, and anchor placement\n• Batch processing mode for multiple selected images",
                    key_learnings="Gained hands-on experience with coordinate transformations, alpha channel compositing in Pillow, and event-driven GUI architecture in Python.",
                    challenges="Maintaining aspect-ratio integrity when rendering large multi-megapixel photos onto a constrained desktop preview window.",
                    future_improvements="Add customizable logo image watermarking in addition to text, plus automatic EXIF metadata preservation.",
                    category="GUI",
                    technologies="Python, Tkinter, Pillow (PIL), Desktop GUI",
                    github_url=None,
                    demo_url=None,
                    featured=True,
                    published=True,
                    order_num=2
                ),
                Project(
                    title="Real-Time Typing Speed Test GUI",
                    slug="typing-speed-gui",
                    summary="An interactive desktop application that measures typing speed in Words Per Minute (WPM) and accuracy in real-time, featuring high-contrast visuals and dynamic passage generators.",
                    description="Developed to practice asynchronous event handling, countdown clocks, and key-press listener loops in desktop Python. The app calculates gross WPM, net WPM, and character accuracy as the user types.",
                    problem="Accurately calculating typing speed requires measuring elapsed keystroke intervals while immediately providing visual feedback on incorrect characters without slowing down the GUI loop.",
                    approach="Engineered a state machine tracking test states (Idle, Active, Completed). Bound `<KeyRelease>` events to a verification algorithm that compares active buffer against the target passage word-by-word.",
                    key_features="• Dynamic passage loading with variable difficulty\n• Live countdown timer and instantaneous WPM recalculation\n• Character-level color feedback (green for correct, red for error)\n• Historical performance scorecard per test session",
                    key_learnings="Mastered Tkinter widget binding, handling millisecond time deltas, and state management in interactive desktop applications.",
                    challenges="Preventing cursor flickering and maintaining synchronized metrics during rapid typing bursts.",
                    future_improvements="Implement local SQLite storage to graph typing speed improvement curves over weeks.",
                    category="GUI",
                    technologies="Python, Tkinter, Time Delta Logic, Event-Driven Programming",
                    github_url=None,
                    demo_url=None,
                    featured=False,
                    published=True,
                    order_num=3
                ),
                Project(
                    title="Breakout Arcade Game Engine",
                    slug="breakout-game",
                    summary="A Python recreation of the classic Atari Breakout arcade game built with Python Turtle graphics, implementing 2D vector collisions, paddle deflection angles, and dynamic brick grids.",
                    description="Created to explore fundamental game loops, 2D vector reflection physics, frame rate governing, and object-oriented component architecture without relying on external heavy game engines.",
                    problem="Simulating realistic ball bounces off different segments of a moving paddle and handling collision detection with dozens of destroyable grid blocks at 60 FPS.",
                    approach="Designed an object-oriented hierarchy: Paddle, Ball, Brick, and Scoreboard classes. Computed deflection angle modifiers based on the offset distance from paddle center upon collision.",
                    key_features="• Responsive paddle movement via keyboard listeners\n• Multi-colored brick grid with score multipliers\n• Dynamic ball speed acceleration as brick count diminishes\n• High-score tracking and live lives counter",
                    key_learnings="Developed concrete intuition for game loop architecture (`screen.update()`), frame rate throttling, Cartesian coordinate collision math, and clean OOP separation.",
                    challenges="Resolving ball tunneling bugs where the ball skipped past brick boundaries during high velocities.",
                    future_improvements="Port the collision engine to Pygame or Flutter Flame engine for mobile touch controls.",
                    category="Games",
                    technologies="Python, Turtle Graphics, OOP, 2D Physics Math",
                    github_url=None,
                    demo_url=None,
                    featured=False,
                    published=True,
                    order_num=4
                ),
                Project(
                    title="Autonomous T-Rex Runner Bot",
                    slug="t-rex-game-automation",
                    summary="An automation project utilizing Python, Selenium, and pixel color sampling to play Chrome's offline Dinosaur game automatically at increasing speeds.",
                    description="Created to explore browser automation, computer vision heuristics, and low-latency decision loops. The bot detects approaching cacti and pterodactyl obstacles and triggers jumps or ducks at calculated distance thresholds.",
                    problem="As the Chrome Dino game progresses, obstacle speeds increase non-linearly. A static sensor point fails after the first 30 seconds of gameplay.",
                    approach="Leveraged Selenium WebDriver to launch the browser environment. Implemented dynamic bounding box sampling that expands the lookahead detection horizon proportional to the elapsed game duration.",
                    key_features="• Automated browser initialization and headless control\n• Fast pixel intensity detection algorithm\n• Adaptive velocity lookahead threshold scaling\n• Automated score recording and crash recovery",
                    key_learnings="Acquired practical understanding of browser DOM hooks, screen capture latency optimization, and feedback control loops.",
                    challenges="Minimizing the round-trip latency between obstacle detection and keyboard event dispatch to prevent missed jumps at high speeds.",
                    future_improvements="Replace pixel heuristic thresholding with a reinforcement learning Q-table agent.",
                    category="Automation",
                    technologies="Python, Selenium, Automation, PIL/Pillow",
                    github_url=None,
                    demo_url=None,
                    featured=True,
                    published=True,
                    order_num=5
                ),
                Project(
                    title="PDF to Audiobook Voice Synthesizer",
                    slug="pdf-text-to-speech",
                    summary="A Python automation tool that extracts textual chapters from PDF documents, performs text cleaning, and converts contents into downloadable MP3 audio files.",
                    description="Built to automate the conversion of academic articles and technical notes into audio for listening during commutes. Leverages PyPDF text stream extraction combined with text-to-speech synthesis.",
                    problem="Raw PDF extraction often produces broken hyphenated words, orphan line breaks, header/footer garbage text, and page numbers that disrupt audio listening flow.",
                    approach="Engineered a multi-stage regex cleaning pipeline to stitch split words across page margins and filter out repetitive page headers before piping the cleaned token stream to the TTS audio synthesizer.",
                    key_features="• Multi-page PDF parsing with page range selection\n• Natural language preprocessing and hyphenation repair\n• Adjustable voice pitch, reading speed, and volume\n• Direct export to standardized MP3 audio tracks",
                    key_learnings="Gained deep practice with regular expression data cleansing, file streaming, and working with audio encoding pipelines in Python.",
                    challenges="Extracting text accurately from multi-column PDF layouts without mixing adjacent article columns together.",
                    future_improvements="Integrate neural voice synthesis APIs and add automatic chapter bookmarking.",
                    category="Automation",
                    technologies="Python, PyPDF, pyttsx3/TTS, Regex Data Cleaning",
                    github_url=None,
                    demo_url=None,
                    featured=False,
                    published=True,
                    order_num=6
                ),
                Project(
                    title="Image Color Palette & HEX Extraction Tool",
                    slug="color-palette-extractor",
                    summary="A data processing script that analyzes uploaded images, clusters predominant pixel colors using numerical arrays, and outputs dominant color palettes with HEX and RGB codes.",
                    description="Developed to bridge image processing and data manipulation. The script ingests photographic images, samples pixel values into NumPy arrays, and identifies the top 10 most prominent colors with their percentage distribution.",
                    problem="Extracting meaningful color palettes from high-resolution images requires grouping similar shades together rather than simply counting raw exact RGB values.",
                    approach="Downsampled input images using Pillow and flattened RGB channels into multidimensional NumPy matrices. Applied frequency binning and color distance thresholds to group near-duplicate shades.",
                    key_features="• Ingests common photo formats (JPEG, PNG, WebP)\n• Calculates percentage representation of dominant colors\n• Generates visual swatch cards alongside exact HEX/RGB values\n• Exportable color schemes for web and UI design inspiration",
                    key_learnings="Applied NumPy array vectorization for fast image computations and learned color space representations (RGB, HSV).",
                    challenges="Balancing computational speed with color clustering accuracy for large 4K image files.",
                    future_improvements="Deploy as an interactive web tool in Flask with interactive color copy-to-clipboard functionality.",
                    category="Data",
                    technologies="Python, NumPy, Pillow, Matplotlib, Data Analysis",
                    github_url=None,
                    demo_url=None,
                    featured=False,
                    published=True,
                    order_num=7
                ),
                Project(
                    title="Space Missions Historical Data Analysis",
                    slug="space-missions-data-analysis",
                    summary="An exploratory data science project analyzing global space launch records from 1957 to present using Pandas, NumPy, and Matplotlib to uncover launch success rates and historical trends.",
                    description="Built to explore exploratory data analysis (EDA) workflows. The project inspects historical launch records across nations, organizations (NASA, Roscosmos, ESA, ISRO, SpaceX), launch vehicles, and mission success ratios.",
                    problem="Historical telemetry datasets suffer from inconsistent organization names, missing mission costs, and varying date formats spanning over 6 decades.",
                    approach="Used Pandas for data cleaning, date-time parsing, and handling null values. Synthesized aggregated metrics and created clear multi-chart visualizations using Matplotlib.",
                    key_features="• Chronological trend analysis of space exploration launches\n• Success vs. failure ratio comparisons by nation and provider\n• Cost-per-launch correlation studies with vehicle reusability\n• Clean publication-ready visual plots with custom styling",
                    key_learnings="Gained practical experience with Pandas groupby operations, data cleaning pipelines, missing value imputation, and Matplotlib layout formatting.",
                    challenges="Reconciling historical state-owned agencies with modern commercial space companies under unified categorical metrics.",
                    future_improvements="Incorporate interactive visual dashboards using Plotly and correlate mission launches with macroeconomic budget data.",
                    category="Data",
                    technologies="Python, Pandas, NumPy, Matplotlib, Data Science",
                    github_url=None,
                    demo_url=None,
                    featured=True,
                    published=True,
                    order_num=8
                ),
                Project(
                    title="Automated Product Price Tracker & Alert Bot",
                    slug="ecommerce-price-tracker",
                    summary="A web scraping automation bot that periodically monitors specific e-commerce product listings using BeautifulSoup and Requests, alerting when price drops below a defined threshold.",
                    description="Created to automate manual shopping research. The bot periodically requests targeted product URLs, extracts currency and price numbers from DOM selectors, and logs historical prices in a local database.",
                    problem="Websites frequently change layout classes, inject dynamic JavaScript, or block repetitive scraping requests without proper HTTP header emulation.",
                    approach="Configured custom HTTP headers with User-Agent rotation. Extracted price elements using BeautifulSoup CSS selectors and sanitized currency symbols into clean floating-point values for threshold comparison.",
                    key_features="• Resilient DOM parsing with fallback CSS selectors\n• Price sanitization across multiple currency formats\n• Local CSV and SQLite price trend tracking\n• Email notification trigger upon target discount detection",
                    key_learnings="Learned realistic web scraping hygiene, HTTP status handling, header spoofing ethics, and automated alert triggering.",
                    challenges="Handling dynamic layout shifts and localized currency symbol formatting variations.",
                    future_improvements="Add proxy support and deploy as a scheduled background worker on a lightweight VPS.",
                    category="Automation",
                    technologies="Python, BeautifulSoup, Requests, Automation, SQLite",
                    github_url=None,
                    demo_url=None,
                    featured=False,
                    published=True,
                    order_num=9
                ),
                Project(
                    title="Minimalist Task Management Web App",
                    slug="flask-task-manager",
                    summary="A clean, responsive CRUD productivity web application developed with Python, Flask, and SQLAlchemy, demonstrating complete database persistence and modular route architecture.",
                    description="Developed as an introduction to full-stack web engineering with Flask. Implemented full CRUD (Create, Read, Update, Delete) workflows, database migrations, and clean CSS styling for personal daily task prioritization.",
                    problem="Overly complicated project management tools often introduce cognitive overhead. A distraction-free, fast-loading task organizer helps maintain daily academic focus.",
                    approach="Structured the backend using Flask Blueprints and SQLAlchemy ORM models. Implemented CSRF token security and responsive card views with subtle completion animations.",
                    key_features="• Clean task creation with categories and due dates\n• One-click task completion toggle and inline deletion\n• Filter views: Active, Completed, High Priority\n• Persistent relational storage via SQLite / SQLAlchemy",
                    key_learnings="Mastered the request-response lifecycle, Jinja2 template inheritance, form validation, and relational database migrations.",
                    challenges="Implementing instantaneous UI state updates without full page reloads while maintaining simple server-rendered architecture.",
                    future_improvements="Add user account authentication and calendar timeline integration.",
                    category="Web",
                    technologies="Python, Flask, SQLAlchemy, Jinja2, CSS3",
                    github_url=None,
                    demo_url=None,
                    featured=False,
                    published=True,
                    order_num=10
                ),
                Project(
                    title="AI-Powered Mobile Application Concepts (Flutter + Python)",
                    slug="ai-mobile-concepts",
                    summary="Architectural prototypes and UI exploration combining Flutter cross-platform mobile interfaces with lightweight Python backend inference APIs.",
                    description="Represents my current technical frontier: learning Flutter and Dart to bridge mobile user experiences with Python-driven backend logic and AI capabilities. Explores client-server JSON serialization and cross-platform mobile design systems.",
                    problem="Many AI models remain confined to desktop Python scripts or Jupyter notebooks. Bringing them to mobile devices requires bridging cross-platform UI engineering with efficient API backends.",
                    approach="Designing responsive mobile screens in Flutter using declarative Dart widgets. Connecting network calls via Dart HTTP clients to Flask REST endpoints processing input data.",
                    key_features="• Clean declarative Flutter UI mockups and widget architectures\n• Asynchronous REST API integration with Python Flask backends\n• Responsive layout behavior across mobile form factors\n• Modular architecture separating mobile client from backend inference logic",
                    key_learnings="Grasping Dart's static typing, widget tree composability, asynchronous `Future` handling, and client-server interface contracts.",
                    challenges="Adapting from procedural and object-oriented Python to Dart's reactive widget composition model.",
                    future_improvements="Build and deploy a complete production-ready mobile utility on Android and iOS.",
                    category="Mobile",
                    technologies="Flutter, Dart, Python, REST APIs, Mobile Architecture",
                    github_url=None,
                    demo_url=None,
                    featured=True,
                    published=True,
                    order_num=11
                )
            ]
            db.session.add_all(projects_data)
            print("✓ Seeded authentic learning and software projects.")

        db.session.commit()
        print("✅ Database seeding successfully finished!")


if __name__ == '__main__':
    seed_database()
