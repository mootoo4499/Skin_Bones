"""
Cross-Database Relationship Mapper for Skin & Bones Project
Manages relationships and data flow between the 4 Neo4j databases
"""

from neo4j_config import Neo4jManager
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CrossDbRelationship:
    """Represents a relationship spanning multiple databases"""
    source_db: str
    source_node_type: str
    source_id: str
    target_db: str
    target_node_type: str
    target_id: str
    relationship_type: str
    properties: Dict
    created_date: datetime

class CrossDatabaseMapper:
    """Manages relationships and mappings between databases"""

    def __init__(self):
        self.manager = Neo4jManager()
        self.relationships: List[CrossDbRelationship] = []

    def connect_all_databases(self) -> bool:
        """Ensure all databases are connected"""
        return self.manager.connect_all()

    # Book → Screenplay Adaptation Mappings
    def map_character_adaptation(
        self,
        book_character_name: str,
        screenplay_character_name: str,
        adaptation_notes: str = ""
    ) -> bool:
        """Map a book character to its screenplay adaptation"""
        try:
            # Verify book character exists
            with self.manager.get_session('book') as session:
                result = session.run(
                    "MATCH (c:Character {name: $name}) RETURN c.name as name",
                    name=book_character_name
                )
                if not result.single():
                    logger.error(f"Book character '{book_character_name}' not found")
                    return False

            # Create character arc in screenplay database
            with self.manager.get_session('screenplay') as session:
                session.run("""
                MERGE (ca:Character_Arc {
                    character_name: $screenplay_name,
                    source_character: $book_name,
                    adaptation_notes: $notes,
                    created_date: datetime()
                })
                """,
                screenplay_name=screenplay_character_name,
                book_name=book_character_name,
                notes=adaptation_notes)

            # Record cross-database relationship
            self.relationships.append(CrossDbRelationship(
                source_db='book',
                source_node_type='Character',
                source_id=book_character_name,
                target_db='screenplay',
                target_node_type='Character_Arc',
                target_id=screenplay_character_name,
                relationship_type='ADAPTED_AS',
                properties={'adaptation_notes': adaptation_notes},
                created_date=datetime.now()
            ))

            logger.info(f"Mapped character: {book_character_name} → {screenplay_character_name}")
            return True

        except Exception as e:
            logger.error(f"Error mapping character adaptation: {e}")
            return False

    def map_scene_adaptation(
        self,
        book_scene_id: str,
        screenplay_scene_number: str,
        adaptation_type: str,
        changes_made: str = ""
    ) -> bool:
        """Map a book scene to its screenplay adaptation"""
        try:
            # Verify book scene exists
            with self.manager.get_session('book') as session:
                result = session.run(
                    "MATCH (s:Scene {scene_id: $scene_id}) RETURN s",
                    scene_id=book_scene_id
                )
                book_scene = result.single()
                if not book_scene:
                    logger.error(f"Book scene '{book_scene_id}' not found")
                    return False

            # Create or update screenplay scene
            with self.manager.get_session('screenplay') as session:
                session.run("""
                MERGE (ss:Screenplay_Scene {scene_number: $scene_number})
                SET ss.adaptation_source = $book_scene_id,
                    ss.adaptation_type = $adaptation_type,
                    ss.changes_made = $changes_made,
                    ss.mapped_date = datetime()
                """,
                scene_number=screenplay_scene_number,
                book_scene_id=book_scene_id,
                adaptation_type=adaptation_type,
                changes_made=changes_made)

            self.relationships.append(CrossDbRelationship(
                source_db='book',
                source_node_type='Scene',
                source_id=book_scene_id,
                target_db='screenplay',
                target_node_type='Screenplay_Scene',
                target_id=screenplay_scene_number,
                relationship_type='BECOMES',
                properties={
                    'adaptation_type': adaptation_type,
                    'changes_made': changes_made
                },
                created_date=datetime.now()
            ))

            logger.info(f"Mapped scene: {book_scene_id} → {screenplay_scene_number}")
            return True

        except Exception as e:
            logger.error(f"Error mapping scene adaptation: {e}")
            return False

    # Expertise → Screenplay Application Mappings
    def apply_technique_to_decision(
        self,
        technique_name: str,
        decision_id: str,
        application_notes: str = ""
    ) -> bool:
        """Record application of an expertise technique to an adaptation decision"""
        try:
            # Verify technique exists
            with self.manager.get_session('expertise') as session:
                result = session.run(
                    "MATCH (t:Technique {name: $name}) RETURN t",
                    name=technique_name
                )
                if not result.single():
                    logger.error(f"Technique '{technique_name}' not found")
                    return False

            # Create application record in screenplay database
            with self.manager.get_session('screenplay') as session:
                session.run("""
                MATCH (ad:Adaptation_Decision {decision_id: $decision_id})
                SET ad.technique_applied = $technique_name,
                    ad.application_notes = $application_notes,
                    ad.technique_applied_date = datetime()
                """,
                decision_id=decision_id,
                technique_name=technique_name,
                application_notes=application_notes)

            self.relationships.append(CrossDbRelationship(
                source_db='expertise',
                source_node_type='Technique',
                source_id=technique_name,
                target_db='screenplay',
                target_node_type='Adaptation_Decision',
                target_id=decision_id,
                relationship_type='APPLIED_TO',
                properties={'application_notes': application_notes},
                created_date=datetime.now()
            ))

            logger.info(f"Applied technique: {technique_name} → {decision_id}")
            return True

        except Exception as e:
            logger.error(f"Error applying technique: {e}")
            return False

    # Examples → Screenplay Reference Mappings
    def reference_example_character(
        self,
        example_film: str,
        example_character_name: str,
        screenplay_character_name: str,
        similarity_notes: str = ""
    ) -> bool:
        """Create reference between example character and screenplay character"""
        try:
            # Find example character
            with self.manager.get_session('examples') as session:
                result = session.run("""
                MATCH (f:Film {title: $film_title})
                MATCH (ec:Example_Character {film_title: $film_title, name: $char_name})
                RETURN ec
                """,
                film_title=example_film,
                char_name=example_character_name)

                if not result.single():
                    logger.error(f"Example character '{example_character_name}' from '{example_film}' not found")
                    return False

            # Record reference in screenplay database
            with self.manager.get_session('screenplay') as session:
                session.run("""
                MATCH (ca:Character_Arc {character_name: $screenplay_char})
                SET ca.reference_character = $example_char,
                    ca.reference_film = $example_film,
                    ca.similarity_notes = $similarity_notes,
                    ca.reference_added_date = datetime()
                """,
                screenplay_char=screenplay_character_name,
                example_char=example_character_name,
                example_film=example_film,
                similarity_notes=similarity_notes)

            self.relationships.append(CrossDbRelationship(
                source_db='examples',
                source_node_type='Example_Character',
                source_id=f"{example_film}:{example_character_name}",
                target_db='screenplay',
                target_node_type='Character_Arc',
                target_id=screenplay_character_name,
                relationship_type='INSPIRES',
                properties={
                    'similarity_notes': similarity_notes,
                    'reference_film': example_film
                },
                created_date=datetime.now()
            ))

            logger.info(f"Referenced example: {example_film}:{example_character_name} → {screenplay_character_name}")
            return True

        except Exception as e:
            logger.error(f"Error creating character reference: {e}")
            return False

    # Query Methods
    def get_character_adaptation_chain(self, book_character_name: str) -> Dict:
        """Get full adaptation chain for a character across all databases"""
        chain = {'book': None, 'screenplay': None, 'references': [], 'techniques': []}

        try:
            # Get book character
            with self.manager.get_session('book') as session:
                result = session.run("""
                MATCH (c:Character {name: $name})
                RETURN c {.*} as character
                """, name=book_character_name)
                record = result.single()
                if record:
                    chain['book'] = record['character']

            # Get screenplay adaptation
            with self.manager.get_session('screenplay') as session:
                result = session.run("""
                MATCH (ca:Character_Arc {source_character: $name})
                RETURN ca {.*} as arc
                """, name=book_character_name)
                record = result.single()
                if record:
                    chain['screenplay'] = record['arc']

            # Get references and techniques from cross-database relationships
            for rel in self.relationships:
                if rel.source_id == book_character_name:
                    if rel.source_db == 'examples':
                        chain['references'].append(rel)
                    elif rel.source_db == 'expertise':
                        chain['techniques'].append(rel)

            return chain

        except Exception as e:
            logger.error(f"Error getting adaptation chain: {e}")
            return chain

    def get_all_cross_database_relationships(self) -> List[Dict]:
        """Get summary of all cross-database relationships"""
        relationships = []

        for rel in self.relationships:
            relationships.append({
                'source': f"{rel.source_db}:{rel.source_node_type}:{rel.source_id}",
                'target': f"{rel.target_db}:{rel.target_node_type}:{rel.target_id}",
                'relationship_type': rel.relationship_type,
                'properties': rel.properties,
                'created_date': rel.created_date.isoformat()
            })

        return relationships

    def validate_all_mappings(self) -> Dict[str, List[str]]:
        """Validate that all cross-database references are still valid"""
        issues = {
            'missing_sources': [],
            'missing_targets': [],
            'connection_errors': []
        }

        for rel in self.relationships:
            try:
                # Check source exists
                with self.manager.get_session(rel.source_db) as session:
                    if rel.source_node_type == 'Character':
                        result = session.run(f"MATCH (n:{rel.source_node_type} {{name: $id}}) RETURN count(n) as count", id=rel.source_id)
                    else:
                        result = session.run(f"MATCH (n:{rel.source_node_type}) WHERE n.scene_id = $id OR n.name = $id RETURN count(n) as count", id=rel.source_id)

                    if result.single()['count'] == 0:
                        issues['missing_sources'].append(f"{rel.source_db}:{rel.source_node_type}:{rel.source_id}")

                # Check target exists
                with self.manager.get_session(rel.target_db) as session:
                    if rel.target_node_type == 'Character_Arc':
                        result = session.run(f"MATCH (n:{rel.target_node_type} {{character_name: $id}}) RETURN count(n) as count", id=rel.target_id)
                    else:
                        result = session.run(f"MATCH (n:{rel.target_node_type}) WHERE n.scene_number = $id OR n.name = $id RETURN count(n) as count", id=rel.target_id)

                    if result.single()['count'] == 0:
                        issues['missing_targets'].append(f"{rel.target_db}:{rel.target_node_type}:{rel.target_id}")

            except Exception as e:
                issues['connection_errors'].append(f"Error validating {rel.source_id} → {rel.target_id}: {e}")

        return issues

    def cleanup(self):
        """Close all database connections"""
        self.manager.close_all()

# Example usage and initial setup
def setup_initial_mappings():
    """Set up initial character and scene mappings for Skin & Bones"""
    mapper = CrossDatabaseMapper()

    if not mapper.connect_all_databases():
        logger.error("Failed to connect to databases")
        return

    try:
        # Map main characters
        character_mappings = [
            ('Lena', 'Lena', 'Protagonist - museum director with body image journey'),
            ('Honey', 'Honey', 'Supporting - complex mother with food/control issues'),
            ('Aaliyah', 'Aaliyah', 'Supporting - child catalyst for family healing'),
            ('Malcolm', 'Malcolm', 'Supporting - fiancé seeking forgiveness'),
            ('Bryan', 'Bryan', 'Supporting - ex returning during crisis'),
            ('Kendra', 'Kendra', 'Supporting - best friend with professional betrayal')
        ]

        for book_name, screen_name, notes in character_mappings:
            mapper.map_character_adaptation(book_name, screen_name, notes)

        # Map key scenes
        scene_mappings = [
            ('opening_doctors_office', '1', 'direct', 'Opening image - establish protagonist state'),
            ('wedding_betrayal', '15', 'direct', 'Catalyst - inciting incident'),
        ]

        for book_scene, screen_scene, adapt_type, notes in scene_mappings:
            mapper.map_scene_adaptation(book_scene, screen_scene, adapt_type, notes)

        logger.info("Initial mappings completed successfully")

        # Validate mappings
        issues = mapper.validate_all_mappings()
        if any(issues.values()):
            logger.warning(f"Validation issues found: {issues}")
        else:
            logger.info("All mappings validated successfully")

    except Exception as e:
        logger.error(f"Error during initial mapping setup: {e}")

    finally:
        mapper.cleanup()

if __name__ == "__main__":
    setup_initial_mappings()