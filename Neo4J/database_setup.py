"""
Database Initialization Script for Skin & Bones Neo4j Knowledge Graph
Creates schema constraints, indexes, and initial data structure
"""

from neo4j_config import Neo4jManager, BookDatabase, ScreenplayDatabase
import logging
from datetime import datetime
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """Handles initialization of all 4 Neo4j databases"""

    def __init__(self):
        self.manager = Neo4jManager()
        self.book_db = BookDatabase(self.manager)
        self.screenplay_db = ScreenplayDatabase(self.manager)

    def initialize_all_databases(self):
        """Initialize schema and constraints for all databases"""
        if not self.manager.connect_all():
            logger.error("Failed to connect to all databases")
            return False

        try:
            self.setup_book_database()
            self.setup_screenplay_database()
            self.setup_expertise_database()
            self.setup_examples_database()
            logger.info("All databases initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False

        finally:
            self.manager.close_all()

    def setup_book_database(self):
        """Initialize the source material database"""
        logger.info("Setting up skinbones_book database...")

        with self.manager.get_session('book') as session:
            # Create constraints
            constraints = [
                "CREATE CONSTRAINT character_name_unique IF NOT EXISTS FOR (c:Character) REQUIRE c.name IS UNIQUE",
                "CREATE CONSTRAINT scene_id_unique IF NOT EXISTS FOR (s:Scene) REQUIRE s.scene_id IS UNIQUE",
                "CREATE CONSTRAINT theme_name_unique IF NOT EXISTS FOR (t:Theme) REQUIRE t.name IS UNIQUE",
                "CREATE CONSTRAINT location_name_unique IF NOT EXISTS FOR (l:Location) REQUIRE l.name IS UNIQUE"
            ]

            # Create indexes
            indexes = [
                "CREATE INDEX character_role_index IF NOT EXISTS FOR (c:Character) ON (c.role)",
                "CREATE INDEX scene_location_index IF NOT EXISTS FOR (s:Scene) ON (s.location)",
                "CREATE INDEX theme_importance_index IF NOT EXISTS FOR (t:Theme) ON (t.importance_level)",
                "CREATE INDEX quote_speaker_index IF NOT EXISTS FOR (q:Quote) ON (q.speaker)"
            ]

            for constraint in constraints:
                session.run(constraint)

            for index in indexes:
                session.run(index)

            # Create initial themes from the story analysis
            themes_data = [
                {
                    'name': 'Identity and Body Image',
                    'description': 'Lenas struggle with weight, self-acceptance, and societal beauty standards',
                    'importance_level': 5,
                    'visual_metaphors': ['mirrors', 'clothing', 'medical settings', 'food']
                },
                {
                    'name': 'Generational Relationships',
                    'description': 'Complex mother-daughter dynamics around control, care, and food',
                    'importance_level': 5,
                    'visual_metaphors': ['kitchen scenes', 'shared meals', 'childhood photos']
                },
                {
                    'name': 'Forgiveness and Betrayal',
                    'description': 'Romantic and friendship conflicts requiring reconciliation',
                    'importance_level': 4,
                    'visual_metaphors': ['wedding dress', 'broken objects', 'distance/proximity']
                },
                {
                    'name': 'Cultural Heritage',
                    'description': 'Reclaiming Black Portland history through museum work',
                    'importance_level': 4,
                    'visual_metaphors': ['museum artifacts', 'church pews', 'historical photos']
                },
                {
                    'name': 'Motherhood and Protection',
                    'description': 'Lenas fears about passing trauma to Aaliyah',
                    'importance_level': 5,
                    'visual_metaphors': ['pills/medication', 'school scenes', 'mirrors reflecting generations']
                }
            ]

            for theme in themes_data:
                session.run("""
                CREATE (t:Theme {
                    name: $name,
                    description: $description,
                    importance_level: $importance_level,
                    visual_metaphors: $visual_metaphors
                })
                """, **theme)

        logger.info("Book database schema created")

    def setup_screenplay_database(self):
        """Initialize the screenplay adaptation database"""
        logger.info("Setting up skinbones_screenplay database...")

        with self.manager.get_session('screenplay') as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT script_version_unique IF NOT EXISTS FOR (sv:Script_Version) REQUIRE sv.version_number IS UNIQUE",
                "CREATE CONSTRAINT decision_id_unique IF NOT EXISTS FOR (ad:Adaptation_Decision) REQUIRE ad.decision_id IS UNIQUE",
                "CREATE CONSTRAINT feedback_id_unique IF NOT EXISTS FOR (f:Feedback) REQUIRE f.feedback_id IS UNIQUE"
            ]

            # Indexes
            indexes = [
                "CREATE INDEX script_status_index IF NOT EXISTS FOR (sv:Script_Version) ON (sv.status)",
                "CREATE INDEX scene_adaptation_type_index IF NOT EXISTS FOR (ss:Screenplay_Scene) ON (ss.adaptation_type)",
                "CREATE INDEX decision_category_index IF NOT EXISTS FOR (ad:Adaptation_Decision) ON (ad.category)",
                "CREATE INDEX feedback_priority_index IF NOT EXISTS FOR (f:Feedback) ON (f.priority)"
            ]

            for constraint in constraints:
                session.run(constraint)

            for index in indexes:
                session.run(index)

            # Create initial script version
            initial_version = {
                'version_number': '0.1.0',
                'date_created': datetime.now().isoformat(),
                'author': 'Claude + Kevin',
                'notes': 'Initial screenplay adaptation setup',
                'page_count': 0,
                'status': 'draft',
                'feedback_incorporated': []
            }

            session.run("""
            CREATE (sv:Script_Version {
                version_number: $version_number,
                date_created: date($date_created),
                author: $author,
                notes: $notes,
                page_count: $page_count,
                status: $status,
                feedback_incorporated: $feedback_incorporated
            })
            """, **initial_version)

        logger.info("Screenplay database schema created")

    def setup_expertise_database(self):
        """Initialize the expertise database"""
        logger.info("Setting up screenplay_expertise database...")

        with self.manager.get_session('expertise') as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT expert_name_unique IF NOT EXISTS FOR (e:Expert) REQUIRE e.name IS UNIQUE",
                "CREATE CONSTRAINT technique_name_unique IF NOT EXISTS FOR (t:Technique) REQUIRE t.name IS UNIQUE"
            ]

            # Indexes
            indexes = [
                "CREATE INDEX expert_specialty_index IF NOT EXISTS FOR (e:Expert) ON (e.specialties)",
                "CREATE INDEX technique_category_index IF NOT EXISTS FOR (t:Technique) ON (t.category)",
                "CREATE INDEX technique_difficulty_index IF NOT EXISTS FOR (t:Technique) ON (t.difficulty_level)"
            ]

            for constraint in constraints:
                session.run(constraint)

            for index in indexes:
                session.run(index)

            # Add some foundational techniques
            techniques_data = [
                {
                    'name': 'Character Arc Mapping',
                    'category': 'character',
                    'description': 'Track character emotional journey across three acts',
                    'when_to_use': 'During character development and scene planning',
                    'difficulty_level': 3
                },
                {
                    'name': 'Book-to-Screen Dialogue Adaptation',
                    'category': 'dialogue',
                    'description': 'Convert internal monologue to visual/spoken language',
                    'when_to_use': 'When adapting prose with heavy internal voice',
                    'difficulty_level': 4
                },
                {
                    'name': 'Theme Visualization',
                    'category': 'visual',
                    'description': 'Translate abstract themes into concrete visual metaphors',
                    'when_to_use': 'Throughout adaptation process for thematic consistency',
                    'difficulty_level': 4
                }
            ]

            for technique in techniques_data:
                session.run("""
                CREATE (t:Technique {
                    name: $name,
                    category: $category,
                    description: $description,
                    when_to_use: $when_to_use,
                    difficulty_level: $difficulty_level
                })
                """, **technique)

        logger.info("Expertise database schema created")

    def setup_examples_database(self):
        """Initialize the examples database"""
        logger.info("Setting up screenplay_examples database...")

        with self.manager.get_session('examples') as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT film_title_year_unique IF NOT EXISTS FOR (f:Film) REQUIRE (f.title, f.year) IS UNIQUE"
            ]

            # Indexes
            indexes = [
                "CREATE INDEX film_genre_index IF NOT EXISTS FOR (f:Film) ON (f.genre)",
                "CREATE INDEX character_archetype_index IF NOT EXISTS FOR (ec:Example_Character) ON (ec.archetype)",
                "CREATE INDEX scene_type_index IF NOT EXISTS FOR (es:Example_Scene) ON (es.scene_type)"
            ]

            for constraint in constraints:
                session.run(constraint)

            for index in indexes:
                session.run(index)

            # Add reference films relevant to adaptation
            reference_films = [
                {
                    'title': 'Precious',
                    'year': 2009,
                    'genre': ['Drama'],
                    'director': 'Lee Daniels',
                    'writer': ['Geoffrey Fletcher'],
                    'adaptation_source': 'Push by Sapphire',
                    'adaptation_type': 'faithful',
                    'awards': ['Academy Award - Best Adapted Screenplay']
                },
                {
                    'title': 'The Color Purple',
                    'year': 1985,
                    'genre': ['Drama'],
                    'director': 'Steven Spielberg',
                    'writer': ['Menno Meyjes'],
                    'adaptation_source': 'The Color Purple by Alice Walker',
                    'adaptation_type': 'faithful'
                }
            ]

            for film in reference_films:
                session.run("""
                CREATE (f:Film {
                    title: $title,
                    year: $year,
                    genre: $genre,
                    director: $director,
                    writer: $writer,
                    adaptation_source: $adaptation_source,
                    adaptation_type: $adaptation_type,
                    awards: $awards
                })
                """, **film)

        logger.info("Examples database schema created")

    def populate_initial_book_data(self):
        """Populate the book database with Skin & Bones characters and scenes"""
        logger.info("Populating initial book data...")

        # Main characters from the story analysis
        characters_data = [
            {
                'name': 'Lena',
                'full_name': 'Lena',
                'age': 35,  # estimated
                'role': 'protagonist',
                'description': 'Black museum director navigating body image and family relationships',
                'physical_traits': ['plus-sized', 'Black', 'dignified presence'],
                'personality_traits': ['intelligent', 'caring', 'self-critical', 'strong', 'protective'],
                'motivations': ['protect Aaliyah', 'preserve Black history', 'find self-acceptance'],
                'fears': ['dying fat', 'failing as mother', 'being erased'],
                'backstory': 'Museum professional with passion for Vanport history',
                'arc_summary': 'Journey from self-doubt to self-acceptance and empowerment',
                'casting_notes': 'DaVine Joy Randolph'
            },
            {
                'name': 'Honey',
                'full_name': 'Honey',
                'age': 60,  # estimated
                'role': 'supporting',
                'description': 'Lenas mother with complex relationship around food and control',
                'physical_traits': ['mature', 'Black', 'authoritative presence'],
                'personality_traits': ['protective', 'traditional', 'well-meaning', 'controlling'],
                'motivations': ['protect daughter', 'maintain family bonds'],
                'fears': ['losing daughter', 'family dissolution'],
                'backstory': 'Raised Lena with love but food-related issues',
                'arc_summary': 'Learns to support daughter differently',
                'casting_notes': 'Angela Bassett'
            },
            {
                'name': 'Aaliyah',
                'full_name': 'Aaliyah',
                'age': 8,
                'role': 'supporting',
                'description': 'Lenas daughter caught between generational patterns',
                'physical_traits': ['young', 'Black', 'innocent'],
                'personality_traits': ['curious', 'perceptive', 'vulnerable'],
                'motivations': ['understand adult world', 'feel secure'],
                'fears': ['family breaking apart', 'school bullying'],
                'backstory': 'Child of divorced parents',
                'arc_summary': 'Catalyst for family healing'
            }
        ]

        for char_data in characters_data:
            self.book_db.create_character(char_data)

        # Key scenes from beat sheet
        scenes_data = [
            {
                'scene_id': 'opening_doctors_office',
                'chapter_reference': 'Opening',
                'location': 'Doctors Office',
                'summary': 'Lena in too-small gown, humiliated, twisting engagement ring',
                'key_dialogue': ['morbidly obese but seems happy'],
                'themes': ['Identity and Body Image'],
                'emotional_tone': 'humiliation, dignity',
                'visual_elements': ['cramped gown', 'tight blood pressure cuff', 'sparkling ring']
            },
            {
                'scene_id': 'wedding_betrayal',
                'chapter_reference': 'Catalyst',
                'location': 'Wedding Venue',
                'summary': 'Malcolm confesses affair moments before ceremony',
                'themes': ['Forgiveness and Betrayal'],
                'emotional_tone': 'shock, devastation',
                'visual_elements': ['wedding dress', 'crack in door', 'frozen moment']
            }
        ]

        with self.manager.get_session('book') as session:
            for scene in scenes_data:
                session.run("""
                CREATE (s:Scene {
                    scene_id: $scene_id,
                    chapter_reference: $chapter_reference,
                    location: $location,
                    summary: $summary,
                    key_dialogue: $key_dialogue,
                    themes: $themes,
                    emotional_tone: $emotional_tone,
                    visual_elements: $visual_elements
                })
                """, **scene)

        # Link characters to scenes
        self.book_db.link_character_to_scene('Lena', 'opening_doctors_office', 'main character')
        self.book_db.link_character_to_scene('Honey', 'opening_doctors_office', 'supporting presence')

        logger.info("Initial book data populated")

def main():
    """Main initialization function"""
    initializer = DatabaseInitializer()

    print("Initializing Neo4j databases for Skin & Bones project...")

    if initializer.initialize_all_databases():
        print("✅ Database initialization completed successfully")

        # Populate initial data
        try:
            if initializer.manager.connect_all():
                initializer.populate_initial_book_data()
                print("✅ Initial data population completed")
            else:
                print("⚠️ Could not populate initial data - connection issues")
        except Exception as e:
            print(f"⚠️ Error during data population: {e}")
        finally:
            initializer.manager.close_all()
    else:
        print("❌ Database initialization failed")

if __name__ == "__main__":
    main()