# Neo4j Database Schemas

## 1. Source Material Database (`skinbones_book`)

### Node Types

#### Character
```cypher
CREATE (:Character {
  name: STRING,
  full_name: STRING,
  age: INTEGER,
  role: STRING, // "protagonist", "antagonist", "supporting", "minor"
  description: TEXT,
  physical_traits: [STRING],
  personality_traits: [STRING],
  motivations: [STRING],
  fears: [STRING],
  backstory: TEXT,
  arc_summary: TEXT,
  casting_notes: STRING // e.g., "Da'Vine Joy Randolph"
})
```

#### Scene
```cypher
CREATE (:Scene {
  scene_id: STRING,
  chapter_reference: STRING,
  page_numbers: [INTEGER],
  location: STRING,
  time_period: STRING,
  summary: TEXT,
  key_dialogue: [TEXT],
  themes: [STRING],
  emotional_tone: STRING,
  visual_elements: [STRING],
  adaptation_notes: TEXT
})
```

#### Theme
```cypher
CREATE (:Theme {
  name: STRING,
  description: TEXT,
  examples: [TEXT],
  visual_metaphors: [STRING],
  importance_level: INTEGER // 1-5 scale
})
```

#### Location
```cypher
CREATE (:Location {
  name: STRING,
  type: STRING, // "interior", "exterior", "symbolic"
  description: TEXT,
  significance: TEXT,
  atmosphere: STRING,
  practical_considerations: TEXT
})
```

#### Quote
```cypher
CREATE (:Quote {
  text: TEXT,
  page_number: INTEGER,
  speaker: STRING,
  context: TEXT,
  adaptation_potential: STRING, // "direct", "modified", "voice-over", "inspiration"
  cinematic_value: TEXT
})
```

### Relationships

```cypher
// Character relationships
(:Character)-[:RELATED_TO {relationship_type, description, evolution}]->(:Character)
(:Character)-[:APPEARS_IN {role_in_scene, emotional_state}]->(:Scene)
(:Character)-[:EMBODIES]->(:Theme)

// Scene structure
(:Scene)-[:TAKES_PLACE_IN]->(:Location)
(:Scene)-[:EXPLORES]->(:Theme)
(:Scene)-[:CONTAINS]->(:Quote)
(:Scene)-[:FOLLOWS {transition_type}]->(:Scene)

// Thematic connections
(:Quote)-[:EXPRESSES]->(:Theme)
(:Location)-[:SYMBOLIZES]->(:Theme)
```

---

## 2. Screenplay Adaptation Database (`skinbones_screenplay`)

### Node Types

#### Script_Version
```cypher
CREATE (:Script_Version {
  version_number: STRING,
  date_created: DATE,
  author: STRING,
  notes: TEXT,
  page_count: INTEGER,
  status: STRING, // "draft", "revision", "final"
  feedback_incorporated: [TEXT]
})
```

#### Screenplay_Scene
```cypher
CREATE (:Screenplay_Scene {
  scene_number: STRING,
  scene_header: STRING, // "INT. HONEY'S KITCHEN - DAY"
  page_number: INTEGER,
  content: TEXT,
  adaptation_source: STRING, // reference to book scene
  adaptation_type: STRING, // "direct", "composite", "original", "reimagined"
  director_notes: TEXT,
  production_notes: TEXT
})
```

#### Character_Arc
```cypher
CREATE (:Character_Arc {
  character_name: STRING,
  act: INTEGER,
  arc_point: STRING, // "inciting_incident", "midpoint", "climax", etc.
  description: TEXT,
  book_reference: STRING,
  changes_made: TEXT,
  justification: TEXT
})
```

#### Adaptation_Decision
```cypher
CREATE (:Adaptation_Decision {
  decision_id: STRING,
  category: STRING, // "character", "plot", "dialogue", "structure"
  description: TEXT,
  rationale: TEXT,
  alternatives_considered: [TEXT],
  impact_assessment: TEXT,
  date_made: DATE
})
```

#### Feedback
```cypher
CREATE (:Feedback {
  feedback_id: STRING,
  source: STRING, // "reader", "producer", "director"
  type: STRING, // "note", "suggestion", "concern"
  content: TEXT,
  priority: STRING, // "high", "medium", "low"
  status: STRING, // "pending", "addressed", "rejected"
  date_received: DATE
})
```

### Relationships

```cypher
(:Script_Version)-[:CONTAINS]->(:Screenplay_Scene)
(:Screenplay_Scene)-[:ADAPTS {adaptation_notes}]->(:Scene) // Cross-DB reference
(:Character_Arc)-[:BELONGS_TO]->(:Script_Version)
(:Adaptation_Decision)-[:AFFECTS]->(:Screenplay_Scene)
(:Feedback)-[:TARGETS]->(:Screenplay_Scene)
(:Feedback)-[:INFLUENCES]->(:Adaptation_Decision)
```

---

## 3. Screenplay Expertise Database (`screenplay_expertise`)

### Node Types

#### Expert
```cypher
CREATE (:Expert {
  name: STRING,
  credentials: [STRING],
  specialties: [STRING], // "adaptation", "character_development", "dialogue"
  notable_works: [STRING],
  contact_info: STRING,
  bio: TEXT
})
```

#### Technique
```cypher
CREATE (:Technique {
  name: STRING,
  category: STRING, // "structure", "character", "dialogue", "visual"
  description: TEXT,
  when_to_use: TEXT,
  examples: [TEXT],
  source: STRING,
  difficulty_level: INTEGER // 1-5
})
```

#### Best_Practice
```cypher
CREATE (:Best_Practice {
  title: STRING,
  category: STRING,
  description: TEXT,
  dos: [STRING],
  donts: [STRING],
  context: STRING, // "adaptation", "character_development", etc.
  source: STRING
})
```

#### Genre_Convention
```cypher
CREATE (:Genre_Convention {
  genre: STRING, // "drama", "family", "coming-of-age"
  convention_type: STRING, // "structure", "character", "tone"
  description: TEXT,
  examples: [STRING],
  flexibility: STRING // "rigid", "flexible", "optional"
})
```

#### Resource
```cypher
CREATE (:Resource {
  title: STRING,
  type: STRING, // "book", "article", "course", "template"
  author: STRING,
  url: STRING,
  summary: TEXT,
  relevance_score: INTEGER, // 1-10
  tags: [STRING]
})
```

### Relationships

```cypher
(:Expert)-[:DEVELOPED]->(:Technique)
(:Expert)-[:RECOMMENDS]->(:Best_Practice)
(:Expert)-[:CREATED]->(:Resource)
(:Technique)-[:APPLIES_TO]->(:Genre_Convention)
(:Best_Practice)-[:SUPPORTS]->(:Technique)
(:Resource)-[:TEACHES]->(:Technique)
```

---

## 4. Screenplay Examples Database (`screenplay_examples`)

### Node Types

#### Film
```cypher
CREATE (:Film {
  title: STRING,
  year: INTEGER,
  genre: [STRING],
  director: STRING,
  writer: [STRING],
  adaptation_source: STRING, // book, play, etc.
  awards: [STRING],
  box_office: STRING,
  critical_reception: STRING,
  adaptation_type: STRING // "faithful", "loose", "reimagined"
})
```

#### Example_Character
```cypher
CREATE (:Example_Character {
  name: STRING,
  film_title: STRING,
  actor: STRING,
  character_type: STRING, // "protagonist", "antagonist", etc.
  archetype: STRING,
  key_traits: [STRING],
  arc_summary: TEXT,
  dialogue_sample: TEXT,
  relevance_notes: TEXT
})
```

#### Example_Scene
```cypher
CREATE (:Example_Scene {
  scene_id: STRING,
  film_title: STRING,
  scene_type: STRING, // "opening", "midpoint", "climax", etc.
  description: TEXT,
  dialogue_excerpt: TEXT,
  techniques_used: [STRING],
  why_effective: TEXT,
  adaptation_lessons: TEXT
})
```

#### Dialogue_Pattern
```cypher
CREATE (:Dialogue_Pattern {
  pattern_name: STRING,
  description: TEXT,
  character_types: [STRING], // which types of characters use this
  emotional_context: [STRING],
  examples: [TEXT],
  effectiveness_notes: TEXT
})
```

#### Structure_Pattern
```cypher
CREATE (:Structure_Pattern {
  pattern_name: STRING, // "three-act", "hero's_journey", etc.
  description: TEXT,
  beats: [STRING],
  genre_suitability: [STRING],
  examples: [STRING],
  adaptation_considerations: TEXT
})
```

### Relationships

```cypher
(:Film)-[:FEATURES]->(:Example_Character)
(:Film)-[:CONTAINS]->(:Example_Scene)
(:Film)-[:FOLLOWS]->(:Structure_Pattern)
(:Example_Character)-[:USES]->(:Dialogue_Pattern)
(:Example_Scene)-[:DEMONSTRATES]->(:Dialogue_Pattern)
(:Example_Character)-[:SIMILAR_TO {similarity_type, notes}]->(:Character) // Cross-DB
```

---

## Cross-Database Relationships

### Key Connections

```cypher
// Book to Screenplay adaptation tracking
(skinbones_book:Character)-[:ADAPTED_AS]->(:skinbones_screenplay:Character_Arc)
(skinbones_book:Scene)-[:BECOMES]->(:skinbones_screenplay:Screenplay_Scene)

// Expertise application
(screenplay_expertise:Technique)-[:APPLIED_TO]->(:skinbones_screenplay:Adaptation_Decision)
(screenplay_expertise:Best_Practice)-[:GUIDES]->(:skinbones_screenplay:Screenplay_Scene)

// Example references
(screenplay_examples:Example_Character)-[:INSPIRES]->(:skinbones_screenplay:Character_Arc)
(screenplay_examples:Example_Scene)-[:REFERENCED_IN]->(:skinbones_screenplay:Screenplay_Scene)

// Learning feedback loop
(skinbones_screenplay:Adaptation_Decision)-[:VALIDATES]->(:screenplay_expertise:Technique)
(skinbones_screenplay:Feedback)-[:CONFIRMS]->(:screenplay_examples:Example_Scene)
```

---

## Database Indexes and Constraints

```cypher
// Unique constraints
CREATE CONSTRAINT character_name_unique FOR (c:Character) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT scene_id_unique FOR (s:Scene) REQUIRE s.scene_id IS UNIQUE;
CREATE CONSTRAINT film_title_year_unique FOR (f:Film) REQUIRE (f.title, f.year) IS UNIQUE;

// Indexes for performance
CREATE INDEX character_role_index FOR (c:Character) ON (c.role);
CREATE INDEX scene_location_index FOR (s:Scene) ON (s.location);
CREATE INDEX theme_importance_index FOR (t:Theme) ON (t.importance_level);
CREATE INDEX script_version_index FOR (sv:Script_Version) ON (sv.version_number);
```