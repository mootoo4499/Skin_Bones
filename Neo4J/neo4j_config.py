"""
Neo4j Multi-Database Configuration for Skin & Bones Project
Handles connections to 4 specialized databases via MCP
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from neo4j import GraphDatabase
import logging

@dataclass
class DatabaseConfig:
    """Configuration for individual Neo4j database"""
    name: str
    uri: str
    username: str
    password: str
    database: str
    description: str

class Neo4jManager:
    """Manages multiple Neo4j database connections for the project"""

    def __init__(self):
        self.drivers: Dict[str, any] = {}
        self.databases = {
            'book': DatabaseConfig(
                name='skinbones_book',
                uri=os.getenv('NEO4J_BOOK_URI', ''),
                username=os.getenv('NEO4J_BOOK_USERNAME', ''),
                password=os.getenv('NEO4J_BOOK_PASSWORD', ''),
                database=os.getenv('NEO4J_BOOK_DATABASE', 'skinbones_book'),
                description='Source material analysis and character/scene storage'
            ),
            'screenplay': DatabaseConfig(
                name='skinbones_screenplay',
                uri=os.getenv('NEO4J_SCREENPLAY_URI', ''),
                username=os.getenv('NEO4J_SCREENPLAY_USERNAME', ''),
                password=os.getenv('NEO4J_SCREENPLAY_PASSWORD', ''),
                database=os.getenv('NEO4J_SCREENPLAY_DATABASE', 'skinbones_screenplay'),
                description='Live screenplay adaptation work and version control'
            ),
            'expertise': DatabaseConfig(
                name='screenplay_expertise',
                uri=os.getenv('NEO4J_EXPERTISE_URI', ''),
                username=os.getenv('NEO4J_EXPERTISE_USERNAME', ''),
                password=os.getenv('NEO4J_EXPERTISE_PASSWORD', ''),
                database=os.getenv('NEO4J_EXPERTISE_DATABASE', 'screenplay_expertise'),
                description='Industry expertise and best practices knowledge base'
            ),
            'examples': DatabaseConfig(
                name='screenplay_examples',
                uri=os.getenv('NEO4J_EXAMPLES_URI', ''),
                username=os.getenv('NEO4J_EXAMPLES_USERNAME', ''),
                password=os.getenv('NEO4J_EXAMPLES_PASSWORD', ''),
                database=os.getenv('NEO4J_EXAMPLES_DATABASE', 'screenplay_examples'),
                description='Reference library of successful screenplays and characters'
            )
        }

        self.logger = logging.getLogger(__name__)

    def connect_all(self) -> bool:
        """Establish connections to all databases"""
        success = True

        for db_key, config in self.databases.items():
            try:
                if not all([config.uri, config.username, config.password]):
                    self.logger.warning(f"Missing credentials for {config.name}")
                    success = False
                    continue

                driver = GraphDatabase.driver(
                    config.uri,
                    auth=(config.username, config.password)
                )

                # Test connection
                with driver.session(database=config.database) as session:
                    result = session.run("RETURN 1 as test")
                    result.single()

                self.drivers[db_key] = driver
                self.logger.info(f"Connected to {config.name}")

            except Exception as e:
                self.logger.error(f"Failed to connect to {config.name}: {e}")
                success = False

        return success

    def get_session(self, database_key: str):
        """Get a session for specific database"""
        if database_key not in self.drivers:
            raise ValueError(f"Database '{database_key}' not connected")

        config = self.databases[database_key]
        return self.drivers[database_key].session(database=config.database)

    def close_all(self):
        """Close all database connections"""
        for db_key, driver in self.drivers.items():
            try:
                driver.close()
                self.logger.info(f"Closed connection to {self.databases[db_key].name}")
            except Exception as e:
                self.logger.error(f"Error closing {db_key}: {e}")

        self.drivers.clear()

    def get_database_info(self) -> Dict[str, Dict]:
        """Get information about all configured databases"""
        info = {}
        for key, config in self.databases.items():
            info[key] = {
                'name': config.name,
                'description': config.description,
                'connected': key in self.drivers,
                'database': config.database
            }
        return info

# Database-specific query helpers
class BookDatabase:
    """Helper methods for the source material database"""

    def __init__(self, neo4j_manager: Neo4jManager):
        self.manager = neo4j_manager
        self.db_key = 'book'

    def create_character(self, character_data: Dict):
        """Create a character node with relationships"""
        with self.manager.get_session(self.db_key) as session:
            query = """
            CREATE (c:Character {
                name: $name,
                full_name: $full_name,
                age: $age,
                role: $role,
                description: $description,
                physical_traits: $physical_traits,
                personality_traits: $personality_traits,
                motivations: $motivations,
                fears: $fears,
                backstory: $backstory,
                arc_summary: $arc_summary,
                casting_notes: $casting_notes
            })
            RETURN c
            """
            return session.run(query, **character_data).single()

    def link_character_to_scene(self, character_name: str, scene_id: str, role_in_scene: str):
        """Create relationship between character and scene"""
        with self.manager.get_session(self.db_key) as session:
            query = """
            MATCH (c:Character {name: $character_name})
            MATCH (s:Scene {scene_id: $scene_id})
            CREATE (c)-[:APPEARS_IN {role_in_scene: $role_in_scene}]->(s)
            """
            session.run(query,
                       character_name=character_name,
                       scene_id=scene_id,
                       role_in_scene=role_in_scene)

class ScreenplayDatabase:
    """Helper methods for the screenplay adaptation database"""

    def __init__(self, neo4j_manager: Neo4jManager):
        self.manager = neo4j_manager
        self.db_key = 'screenplay'

    def create_script_version(self, version_data: Dict):
        """Create a new script version"""
        with self.manager.get_session(self.db_key) as session:
            query = """
            CREATE (sv:Script_Version {
                version_number: $version_number,
                date_created: date($date_created),
                author: $author,
                notes: $notes,
                page_count: $page_count,
                status: $status,
                feedback_incorporated: $feedback_incorporated
            })
            RETURN sv
            """
            return session.run(query, **version_data).single()

    def track_adaptation_decision(self, decision_data: Dict):
        """Record an adaptation decision with rationale"""
        with self.manager.get_session(self.db_key) as session:
            query = """
            CREATE (ad:Adaptation_Decision {
                decision_id: $decision_id,
                category: $category,
                description: $description,
                rationale: $rationale,
                alternatives_considered: $alternatives_considered,
                impact_assessment: $impact_assessment,
                date_made: date($date_made)
            })
            RETURN ad
            """
            return session.run(query, **decision_data).single()

# Environment setup helper
def setup_environment_file():
    """Generate .env template for Neo4j credentials"""
    env_template = """
# Neo4j Database Configurations for Skin & Bones Project

# Source Material Database (skinbones_book)
NEO4J_BOOK_URI=bolt://localhost:7687
NEO4J_BOOK_USERNAME=neo4j
NEO4J_BOOK_PASSWORD=your_password_here
NEO4J_BOOK_DATABASE=skinbones_book

# Screenplay Adaptation Database (skinbones_screenplay)
NEO4J_SCREENPLAY_URI=bolt://localhost:7687
NEO4J_SCREENPLAY_USERNAME=neo4j
NEO4J_SCREENPLAY_PASSWORD=your_password_here
NEO4J_SCREENPLAY_DATABASE=skinbones_screenplay

# Expertise Database (screenplay_expertise)
NEO4J_EXPERTISE_URI=bolt://localhost:7687
NEO4J_EXPERTISE_USERNAME=neo4j
NEO4J_EXPERTISE_PASSWORD=your_password_here
NEO4J_EXPERTISE_DATABASE=screenplay_expertise

# Examples Database (screenplay_examples)
NEO4J_EXAMPLES_URI=bolt://localhost:7687
NEO4J_EXAMPLES_USERNAME=neo4j
NEO4J_EXAMPLES_PASSWORD=your_password_here
NEO4J_EXAMPLES_DATABASE=screenplay_examples
    """

    with open('.env.template', 'w') as f:
        f.write(env_template.strip())

    print("Created .env.template file. Copy to .env and fill in your credentials.")

if __name__ == "__main__":
    # Example usage
    manager = Neo4jManager()

    # Generate environment template
    setup_environment_file()

    # Display database configuration info
    print("Database Configuration:")
    for key, info in manager.get_database_info().items():
        print(f"  {key}: {info['name']} - {info['description']}")