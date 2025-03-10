"""
AI CEO Management System - AI Legal Team
Provides legal assistance to bail bond users and ensures compliance with laws
"""
import os
import json
import logging
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AILegalTeam")

class LegalCase:
    """Represents a legal case with associated documents and status updates"""
    def __init__(self, case_id, user_id, defendant_name, bail_bond_id, charges, court_date, court_location):
        self.case_id = case_id
        self.user_id = user_id
        self.defendant_name = defendant_name
        self.bail_bond_id = bail_bond_id
        self.charges = charges if charges else []
        self.court_date = court_date
        self.court_location = court_location
        self.status = "active"
        self.notes = []
        self.documents = []
        self.appearances = []
        self.legal_team = []
        self.created_date = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()
    
    def add_note(self, note_text, author="AI Legal Assistant"):
        """Add a note to the case"""
        note = {
            "text": note_text,
            "author": author,
            "timestamp": datetime.now().isoformat()
        }
        self.notes.append(note)
        self.last_updated = datetime.now().isoformat()
        return note
    
    def add_document(self, doc_type, title, content, is_template=False):
        """Add a document to the case"""
        document = {
            "doc_id": f"doc_{len(self.documents) + 1}",
            "type": doc_type,
            "title": title,
            "content": content,
            "is_template": is_template,
            "created_date": datetime.now().isoformat(),
            "version": 1
        }
        self.documents.append(document)
        self.last_updated = datetime.now().isoformat()
        return document
    
    def add_court_appearance(self, appearance_date, appearance_type, notes=None):
        """Add a court appearance to the case"""
        appearance = {
            "appearance_id": f"app_{len(self.appearances) + 1}",
            "date": appearance_date.isoformat() if isinstance(appearance_date, datetime) else appearance_date,
            "type": appearance_type,
            "notes": notes or [],
            "status": "scheduled"
        }
        self.appearances.append(appearance)
        self.last_updated = datetime.now().isoformat()
        return appearance
    
    def assign_legal_team(self, team_members):
        """Assign legal team members to the case"""
        self.legal_team = team_members
        self.last_updated = datetime.now().isoformat()
        return self.legal_team
    
    def update_status(self, status):
        """Update the case status"""
        self.status = status
        self.last_updated = datetime.now().isoformat()
        return self.status
    
    def to_dict(self):
        """Convert case to dictionary for serialization"""
        return {
            "case_id": self.case_id,
            "user_id": self.user_id,
            "defendant_name": self.defendant_name,
            "bail_bond_id": self.bail_bond_id,
            "charges": self.charges,
            "court_date": self.court_date,
            "court_location": self.court_location,
            "status": self.status,
            "notes": self.notes,
            "documents": self.documents,
            "appearances": self.appearances,
            "legal_team": self.legal_team,
            "created_date": self.created_date,
            "last_updated": self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create case from dictionary"""
        case = cls(
            data["case_id"],
            data["user_id"],
            data["defendant_name"],
            data["bail_bond_id"],
            data["charges"],
            data["court_date"],
            data["court_location"]
        )
        case.status = data["status"]
        case.notes = data["notes"]
        case.documents = data["documents"]
        case.appearances = data["appearances"]
        case.legal_team = data["legal_team"]
        case.created_date = data["created_date"]
        case.last_updated = data["last_updated"]
        return case

class LegalDocumentGenerator:
    """Generates legal documents based on case information and templates"""
    def __init__(self, templates_dir="legal_templates"):
        self.templates_dir = templates_dir
        
        # Create templates directory if it doesn't exist
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
            self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default legal document templates"""
        default_templates = {
            "court_appearance_reminder": """
NOTICE OF COURT APPEARANCE

CASE NUMBER: {case_number}
DEFENDANT: {defendant_name}

This is a reminder that you are scheduled to appear in court on:
Date: {court_date}
Time: {court_time}
Location: {court_location}
Department: {department}

Please arrive at least 30 minutes early to clear security and locate your courtroom.
Failure to appear may result in a warrant being issued for your arrest and forfeiture
of your bail bond.

If you have any questions, please contact your AI Legal Team at:
Phone: (800) BAIL-CEO
Email: legal@aiceo.com

Sincerely,
AI CEO Legal Team
""",
            "bail_conditions_reminder": """
BAIL CONDITIONS REMINDER

CASE NUMBER: {case_number}
DEFENDANT: {defendant_name}
BAIL BOND ID: {bail_bond_id}

This is a reminder of the conditions of your bail:

1. You must appear at all scheduled court appearances
2. You must not leave the jurisdiction without court permission
3. You must report to your AI Monitoring System as scheduled
4. {additional_conditions}

Compliance with these conditions is monitored through our AI tracking systems.
Violation of any condition may result in revocation of bail and return to custody.

Your next check-in is scheduled for: {next_checkin_date}

If you have any questions, please contact your AI Legal Team at:
Phone: (800) BAIL-CEO
Email: legal@aiceo.com

Sincerely,
AI CEO Legal Team
""",
            "motion_to_dismiss": """
IN THE {court_name}
{county} COUNTY, {state}

THE PEOPLE OF THE STATE OF {state},
                   Plaintiff,
v.
{defendant_name},
                   Defendant.

CASE NO. {case_number}

MOTION TO DISMISS

COMES NOW the Defendant, {defendant_name}, by and through the undersigned AI Legal Team,
and moves this Honorable Court to dismiss the {charge} against the Defendant, and as
grounds therefore states:

1. {argument_1}
2. {argument_2}
3. {argument_3}

WHEREFORE, the Defendant respectfully requests that this Court dismiss the {charge}
against the Defendant.

Respectfully submitted,

______________________
AI CEO Legal Team
Bar No. AI-{state}-12345
legal@aiceo.com
(800) BAIL-CEO

CERTIFICATE OF SERVICE

I HEREBY CERTIFY that a true and correct copy of the foregoing has been furnished to
the Office of the State Attorney on this {date}.

______________________
AI CEO Legal Team
"""
        }
        
        for template_name, template_content in default_templates.items():
            template_path = os.path.join(self.templates_dir, f"{template_name}.txt")
            with open(template_path, 'w') as f:
                f.write(template_content)
    
    def get_template(self, template_name):
        """Get a document template by name"""
        template_path = os.path.join(self.templates_dir, f"{template_name}.txt")
        
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                return f.read()
        else:
            logger.error(f"Template {template_name} not found")
            return None
    
    def generate_document(self, template_name, context):
        """Generate a document from a template with context variables"""
        template = self.get_template(template_name)
        
        if not template:
            return None
        
        try:
            # Format the template with the provided context
            document = template.format(**context)
            return document
        except KeyError as e:
            logger.error(f"Missing context variable in template: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error generating document: {str(e)}")
            return None
    
    def generate_court_appearance_reminder(self, case):
        """Generate a court appearance reminder document"""
        next_appearance = None
        for appearance in case.appearances:
            appearance_date = datetime.fromisoformat(appearance["date"]) if isinstance(appearance["date"], str) else appearance["date"]
            if appearance["status"] == "scheduled" and appearance_date > datetime.now():
                next_appearance = appearance
                break
        
        if not next_appearance:
            logger.warning(f"No upcoming court appearances found for case {case.case_id}")
            return None
        
        appearance_date = datetime.fromisoformat(next_appearance["date"]) if isinstance(next_appearance["date"], str) else next_appearance["date"]
        context = {
            "case_number": case.case_id,
            "defendant_name": case.defendant_name,
            "court_date": appearance_date.strftime("%B %d, %Y"),
            "court_time": appearance_date.strftime("%I:%M %p"),
            "court_location": case.court_location,
            "department": "Dept. 5"  # This could be dynamic based on case data
        }
        
        return self.generate_document("court_appearance_reminder", context)
    
    def generate_bail_conditions_reminder(self, case, bail_bond):
        """Generate a bail conditions reminder document"""
        # Determine next check-in date (example: 7 days from now)
        next_checkin = datetime.now() + timedelta(days=7)
        
        # Get additional conditions from bail bond data
        additional_conditions = "You must comply with all conditions specified by the court"
        if bail_bond and "conditions" in bail_bond:
            additional_conditions = bail_bond["conditions"]
        
        context = {
            "case_number": case.case_id,
            "defendant_name": case.defendant_name,
            "bail_bond_id": case.bail_bond_id,
            "additional_conditions": additional_conditions,
            "next_checkin_date": next_checkin.strftime("%B %d, %Y at %I:%M %p")
        }
        
        return self.generate_document("bail_conditions_reminder", context)
    
    def generate_motion_to_dismiss(self, case, arguments):
        """Generate a motion to dismiss document"""
        if not case.charges or len(case.charges) == 0:
            logger.warning(f"No charges found for case {case.case_id}")
            return None
        
        charge = case.charges[0] if isinstance(case.charges[0], str) else case.charges[0].get("charge", "Unknown Charge")
        
        # Extract location information from court location
        court_parts = case.court_location.split(",")
        county = "Unknown"
        state = "CA"  # Default to California
        if len(court_parts) >= 2:
            county = court_parts[0].strip()
            state_part = court_parts[1].strip()
            state = state_part[:2]  # Extract state abbreviation
        
        context = {
            "court_name": "SUPERIOR COURT",
            "county": county,
            "state": state,
            "defendant_name": case.defendant_name,
            "case_number": case.case_id,
            "charge": charge,
            "argument_1": arguments[0] if len(arguments) > 0 else "Insufficient evidence to support the charge",
            "argument_2": arguments[1] if len(arguments) > 1 else "Violation of defendant's constitutional rights",
            "argument_3": arguments[2] if len(arguments) > 2 else "Interests of justice require dismissal",
            "date": datetime.now().strftime("%dth day of %B, %Y")
        }
        
        return self.generate_document("motion_to_dismiss", context)

class LegalReferenceLibrary:
    """
    Provides access to legal resources, case law, and statutes
    related to bail bonds and criminal defense
    """
    def __init__(self, cache_dir="legal_cache"):
        self.cache_dir = cache_dir
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        # Initialize common legal resource URLs
        self.legal_resources = {
            "federal_rules": "https://www.law.cornell.edu/rules/frcrmp",
            "bail_statutes": "https://www.law.cornell.edu/uscode/text/18/3142",
            "case_law_search": "https://www.courtlistener.com/api/rest/v3/search/?type=o&q={query}"
        }
        
        # Initialize state-specific bail laws
        self.state_bail_laws = {
            "CA": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=1268",
            "NY": "https://www.nysenate.gov/legislation/laws/CPL/510.10",
            "TX": "https://statutes.capitol.texas.gov/Docs/CR/htm/CR.17.htm",
            "FL": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0900-0999/0903/0903.html",
            # Add more states as needed
        }
    
    def search_case_law(self, query, jurisdiction=None, limit=5):
        """
        Search for relevant case law based on query
        
        Args:
            query (str): Search query
            jurisdiction (str, optional): Jurisdiction to limit search (e.g., "ca")
            limit (int, optional): Maximum number of results to return
            
        Returns:
            list: List of relevant case law results
        """
        # Create a cache key for this search
        cache_key = f"case_law_{query.replace(' ', '_')}_{jurisdiction or 'all'}_{limit}"
        cache_file = os.path.join(self.cache_dir, cache_key + ".json")
        
        # Check cache first
        if os.path.exists(cache_file):
            # Check if cache is fresh (less than 1 day old)
            if time.time() - os.path.getmtime(cache_file) < 86400:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    logger.error(f"Error reading cache: {str(e)}")
        
        # Prepare search query
        search_query = query
        if jurisdiction:
            search_query = f"{query} jurisdiction:{jurisdiction}"
        
        # In a real implementation, this would use the Court Listener API or similar
        # For now, we'll return placeholder results for demonstration
        results = [
            {
                "case_name": "United States v. Salerno",
                "citation": "481 U.S. 739 (1987)",
                "summary": "The Supreme Court upheld the constitutionality of the Bail Reform Act of 1984, which allowed for pretrial detention without bail for defendants considered dangerous to the community.",
                "jurisdiction": "US Supreme Court",
                "date": "1987-05-26",
                "url": "https://supreme.justia.com/cases/federal/us/481/739/"
            },
            {
                "case_name": "Stack v. Boyle",
                "citation": "342 U.S. 1 (1951)",
                "summary": "The Supreme Court established that bail cannot be set higher than an amount reasonably calculated to ensure the defendant's presence at trial.",
                "jurisdiction": "US Supreme Court",
                "date": "1951-11-05",
                "url": "https://supreme.justia.com/cases/federal/us/342/1/"
            },
            {
                "case_name": "Bell v. Wolfish",
                "citation": "441 U.S. 520 (1979)",
                "summary": "The Supreme Court ruled that pretrial detention does not constitute punishment before trial, but is a regulatory function of the government.",
                "jurisdiction": "US Supreme Court",
                "date": "1979-05-14",
                "url": "https://supreme.justia.com/cases/federal/us/441/520/"
            },
            {
                "case_name": "In re Humphrey",
                "citation": "11 Cal.5th 135 (2021)",
                "summary": "The California Supreme Court ruled that courts must consider a defendant's ability to pay when setting bail, and cannot detain someone solely because they cannot afford bail.",
                "jurisdiction": "California Supreme Court",
                "date": "2021-03-25",
                "url": "https://law.justia.com/cases/california/supreme-court/2021/s247278.html"
            },
            {
                "case_name": "ODonnell v. Harris County",
                "citation": "892 F.3d 147 (5th Cir. 2018)",
                "summary": "The Fifth Circuit ruled that Harris County's bail system unconstitutionally discriminated against indigent defendants by detaining them solely because they could not afford bail.",
                "jurisdiction": "5th Circuit",
                "date": "2018-06-01",
                "url": "https://www.ca5.uscourts.gov/opinions/pub/17/17-20333-CV0.pdf"
            }
        ]
        
        # Filter by jurisdiction if specified
        if jurisdiction:
            results = [r for r in results if jurisdiction.upper() in r.get("jurisdiction", "").upper()]
        
        # Limit results
        results = results[:limit]
        
        # Cache results
        try:
            with open(cache_file, 'w') as f:
                json.dump(results, f, indent=4)
        except Exception as e:
            logger.error(f"Error caching results: {str(e)}")
        
        return results
    
    def get_bail_statute(self, state_code):
        """
        Get bail statutes for a specific state
        
        Args:
            state_code (str): Two-letter state code (e.g., "CA")
            
        Returns:
            dict: Bail statute information
        """
        state_code = state_code.upper()
        
        # Create a cache key for this state
        cache_key = f"bail_statute_{state_code}"
        cache_file = os.path.join(self.cache_dir, cache_key + ".json")
        
        # Check cache first
        if os.path.exists(cache_file):
            # Check if cache is fresh (less than 7 days old)
            if time.time() - os.path.getmtime(cache_file) < 604800:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    logger.error(f"Error reading cache: {str(e)}")
        
        # Get the URL for this state's bail laws
        bail_law_url = self.state_bail_laws.get(state_code)
        
        if not bail_law_url:
            logger.warning(f"No bail statute URL found for state {state_code}")
            return {
                "state": state_code,
                "found": False,
                "message": f"No bail statute information available for {state_code}"
            }
        
        # In a real implementation, this would scrape the actual statute text
        # For now, we'll return placeholder content for demonstration
        statute_info = {
            "state": state_code,
            "found": True,
            "title": f"{state_code} Bail Statutes",
            "sections": [
                {
                    "section": "1268",
                    "title": "Release on Bail",
                    "text": "Bail is a unilateral contract that allows for the release of a defendant from custody, while ensuring the defendant's appearance in court when required.",
                    "url": self.state_bail_laws.get(state_code, "")
                },
                {
                    "section": "1269",
                    "title": "Taking of Bail",
                    "text": "The defendant may be admitted to bail from the time of the defendant's arrest until a judgment is pronounced, if eligible for bail.",
                    "url": self.state_bail_laws.get(state_code, "")
                },
                {
                    "section": "1270",
                    "title": "Release on Own Recognizance",
                    "text": "A defendant may be released on his or her own recognizance at the discretion of the court.",
                    "url": self.state_bail_laws.get(state_code, "")
                },
                {
                    "section": "1275",
                    "title": "Setting, Reducing, or Denying Bail",
                    "text": "In setting, reducing, or denying bail, the judge or magistrate shall consider the protection of the public, the seriousness of the offense charged, the previous criminal record of the defendant, and the probability of the defendant appearing at trial or at a hearing.",
                    "url": self.state_bail_laws.get(state_code, "")
                }
            ],
            "last_updated": "2023-01-01"
        }
        
        # Cache results
        try:
            with open(cache_file, 'w') as f:
                json.dump(statute_info, f, indent=4)
        except Exception as e:
            logger.error(f"Error caching statute info: {str(e)}")
        
        return statute_info
    
    def get_court_procedures(self, court_name, jurisdiction):
        """
        Get procedures for a specific court
        
        Args:
            court_name (str): Name of the court
            jurisdiction (str): Jurisdiction (state or federal)
            
        Returns:
            dict: Court procedure information
        """
        # Create a cache key for this court
        cache_key = f"court_procedures_{court_name.replace(' ', '_')}_{jurisdiction}"
        cache_file = os.path.join(self.cache_dir, cache_key + ".json")
        
        # Check cache first
        if os.path.exists(cache_file):
            # Check if cache is fresh (less than 30 days old)
            if time.time() - os.path.getmtime(cache_file) < 2592000:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    logger.error(f"Error reading cache: {str(e)}")
        
        # In a real implementation, this would fetch and parse court procedures
        # For now, we'll return placeholder content for demonstration
        court_procedures = {
            "court_name": court_name,
            "jurisdiction": jurisdiction,
            "general_rules": [
                "All parties must be on time for court appearances",
                "Proper attire is required in the courtroom",
                "All electronic devices must be silenced or turned off",
                "No food or drink is allowed in the courtroom",
                "Address the judge as 'Your Honor'"
            ],
            "arraignment_procedures": [
                "Defendants must be present for arraignment unless waived by counsel",
                "The charges will be read aloud in court",
                "The defendant will enter a plea (not guilty, guilty, or no contest)",
                "Bail will be set or continued if already posted",
                "Future court dates will be scheduled"
            ],
            "bail_procedures": [
                "Bail may be posted in cash or through a surety bond",
                "The defendant must provide identification when posting bail",
                "The defendant must sign a promise to appear for all court dates",
                "Bail may be forfeited if the defendant fails to appear",
                "Bail may be modified by filing a motion with the court"
            ],
            "trial_procedures": [
                "Jury selection begins with voir dire",
                "Opening statements are made by both prosecution and defense",
                "The prosecution presents its case first, followed by the defense",
                "Both sides make closing arguments",
                "The jury deliberates and returns a verdict"
            ],
            "court_contact": {
                "address": "123 Legal Ave, Courthouse Plaza",
                "phone": "(555) 123-4567",
                "hours": "Monday-Friday, 8:30am-4:30pm",
                "website": "https://courts.example.gov"
            }
        }
        
        # Cache results
        try:
            with open(cache_file, 'w') as f:
                json.dump(court_procedures, f, indent=4)
        except Exception as e:
            logger.error(f"Error caching court procedures: {str(e)}")
        
        return court_procedures
    
    def search_legal_definitions(self, term):
        """
        Search for legal definitions of terms
        
        Args:
            term (str): Legal term to define
            
        Returns:
            dict: Definition and related information
        """
        # Create a cache key for this term
        cache_key = f"legal_def_{term.replace(' ', '_')}"
        cache_file = os.path.join(self.cache_dir, cache_key + ".json")
        
        # Check cache first
        if os.path.exists(cache_file):
            # Check if cache is fresh (less than a year old)
            if time.time() - os.path.getmtime(cache_file) < 31536000:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    logger.error(f"Error reading cache: {str(e)}")
        
        # In a real implementation, this would search legal dictionaries
        # For now, we'll return placeholder definitions for common bail-related terms
        legal_terms = {
            "bail": {
                "term": "Bail",
                "definition": "Money or property given to a court to secure a defendant's temporary release from jail and ensure their appearance at future court proceedings.",
                "see_also": ["bail bond", "surety", "own recognizance"],
                "sources": ["Black's Law Dictionary", "Federal Rules of Criminal Procedure"]
            },
            "bail bond": {
                "term": "Bail Bond",
                "definition": "A written promise signed by a defendant and surety to ensure that a defendant will appear in court as required, or forfeit the money/collateral set by the court.",
                "see_also": ["bail", "surety", "collateral"],
                "sources": ["Black's Law Dictionary"]
            },
            "surety": {
                "term": "Surety",
                "definition": "A person who agrees to be responsible for the debt or obligation of another. In bail context, the bail bondsman or bail bond agency that issues a bail bond.",
                "see_also": ["bail bond", "indemnitor"],
                "sources": ["Black's Law Dictionary"]
            },
            "arraignment": {
                "term": "Arraignment",
                "definition": "A court proceeding in which a defendant is formally advised of the charges against them and asked to enter a plea of guilty or not guilty.",
                "see_also": ["plea", "indictment", "preliminary hearing"],
                "sources": ["Federal Rules of Criminal Procedure Rule 10"]
            },
            "own recognizance": {
                "term": "Own Recognizance (OR)",
                "definition": "Release of a defendant without the requirement to post bail, based on the defendant's promise to appear at all required court proceedings.",
                "see_also": ["bail", "pretrial release"],
                "sources": ["Federal Rules of Criminal Procedure"]
            },
            "pretrial release": {
                "term": "Pretrial Release",
                "definition": "The release of a defendant from custody pending trial, which may be secured through bail, bond, or release on own recognizance.",
                "see_also": ["bail", "detention hearing"],
                "sources": ["Bail Reform Act of 1984"]
            },
            "bail forfeiture": {
                "term": "Bail Forfeiture",
                "definition": "The loss of the bail money or property when a defendant fails to appear in court as required.",
                "see_also": ["bail jumping", "exoneration"],
                "sources": ["Federal Rules of Criminal Procedure Rule 46"]
            },
            "exoneration": {
                "term": "Exoneration",
                "definition": "The release of a surety from liability on a bail bond, usually after the case is concluded or the defendant is surrendered.",
                "see_also": ["bail", "surety"],
                "sources": ["Black's Law Dictionary"]
            }
        }
        
        term_lower = term.lower()
        result = legal_terms.get(term_lower, {
            "term": term,
            "definition": "Definition not found in our database.",
            "see_also": [],
            "sources": []
        })
        
        # Cache results
        try:
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=4)
        except Exception as e:
            logger.error(f"Error caching legal definition: {str(e)}")
        
        return result

class AILegalTeam:
    """
    Main class that provides comprehensive legal assistance to users on bail
    and ensures compliance with applicable laws
    """
    def __init__(self, config_file="ai_legal_team_config.json", debug_mode=False):
        """Initialize the AI legal team"""
        self.config_file = config_file
        self.debug_mode = debug_mode
        self.config = self._load_config()
        
        # Create data directories
        self.data_dir = "legal_team_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialize components
        self.document_generator = LegalDocumentGenerator()
        self.legal_library = LegalReferenceLibrary()
        
        # Load cases
        self.cases = self._load_cases()
        
        # Legal team members (AI specialists)
        self.team_members = [
            {
                "id": "ai_attorney_criminal",
                "name": "AI Defense Attorney",
                "specialization": "Criminal Defense",
                "bio": "Specialized in criminal defense with expertise in bail proceedings and pretrial motions."
            },
            {
                "id": "ai_paralegal_research",
                "name": "AI Legal Researcher",
                "specialization": "Legal Research",
                "bio": "Specialized in researching case law, statutes, and legal precedents relevant to bail and criminal proceedings."
            },
            {
                "id": "ai_paralegal_compliance",
                "name": "AI Compliance Specialist",
                "specialization": "Regulatory Compliance",
                "bio": "Specialized in ensuring compliance with court orders, bail conditions, and monitoring requirements."
            },
            {
                "id": "ai_advisor_strategy",
                "name": "AI Strategy Advisor",
                "specialization": "Case Strategy",
                "bio": "Specialized in developing optimal legal strategies and evaluating plea options."
            }
        ]
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                if self.debug_mode:
                    print(f"Config file {self.config_file} not found, using defaults")
                default_config = {
                    "version": "1.0.0",
                    "team_size": 4,
                    "auto_document_generation": True,
                    "remind_court_dates": True,
                    "court_reminder_days_ahead": 3,
                    "legal_databases": ["caselaw", "statutes", "regulations"],
                    "supported_jurisdictions": ["federal", "CA", "NY", "TX", "FL"]
                }
                # Save default config
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading config: {str(e)}")
            return {}
    
    def _load_cases(self):
        """Load cases from file"""
        cases_file = os.path.join(self.data_dir, "cases.json")
        try:
            if os.path.exists(cases_file):
                with open(cases_file, 'r') as f:
                    cases_data = json.load(f)
                cases = {}
                for case_id, case_data in cases_data.items():
                    cases[case_id] = LegalCase.from_dict(case_data)
                return cases
            else:
                return {}
        except Exception as e:
            logger.error(f"Error loading cases: {str(e)}")
            return {}
    
    def _save_cases(self):
        """Save cases to file"""
        cases_file = os.path.join(self.data_dir, "cases.json")
        try:
            cases_data = {case_id: case.to_dict() for case_id, case in self.cases.items()}
            with open(cases_file, 'w') as f:
                json.dump(cases_data, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving cases: {str(e)}")
            return False
    
    def create_case(self, user_id, defendant_name, bail_bond_id, charges, court_date, court_location):
        """
        Create a new legal case
        
        Args:
            user_id (str): User ID of the bail bond holder
            defendant_name (str): Name of the defendant
            bail_bond_id (str): Bail bond ID
            charges (list): List of charges against the defendant
            court_date (str): Date of the first court appearance
            court_location (str): Location of the court
            
        Returns:
            LegalCase: The created case
        """
        # Generate a unique case ID
        case_id = f"case_{len(self.cases) + 1}_{int(time.time())}"
        
        # Create the case
        case = LegalCase(
            case_id,
            user_id,
            defendant_name,
            bail_bond_id,
            charges,
            court_date,
            court_location
        )
        
        # Assign legal team members
        case.assign_legal_team(self.team_members)
        
        # Add initial arraignment appearance
        court_date_obj = datetime.fromisoformat(court_date) if isinstance(court_date, str) else court_date
        case.add_court_appearance(court_date_obj, "Arraignment")
        
        # Add welcome note
        case.add_note(
            f"Welcome to your AI Legal Team. We are here to assist with your case related to bail bond #{bail_bond_id}. "
            f"Your first court appearance is scheduled for {court_date_obj.strftime('%B %d, %Y')} at {court_location}. "
            f"We will help ensure you understand all bail conditions and court procedures."
        )
        
        # Generate and add initial documents
        self._create_initial_documents(case)
        
        # Save the case
        self.cases[case_id] = case
        self._save_cases()
        
        return case
    
    def _create_initial_documents(self, case):
        """Create initial documents for a new case"""
        # Add bail conditions document
        bail_conditions = self.document_generator.generate_bail_conditions_reminder(case, None)
        if bail_conditions:
            case.add_document("bail_conditions", "Bail Conditions and Requirements", bail_conditions)
        
        # Add court appearance reminder
        court_reminder = self.document_generator.generate_court_appearance_reminder(case)
        if court_reminder:
            case.add_document("court_reminder", "Court Appearance Reminder", court_reminder)
        
        # Add rights and responsibilities document
        rights_doc = """
DEFENDANT'S RIGHTS AND RESPONSIBILITIES

As a defendant released on bail, you have the following RIGHTS:

1. Right to counsel: You have the right to be represented by an attorney. If you cannot afford one, the court will appoint an attorney to represent you.

2. Right to remain silent: You have the right to remain silent and not incriminate yourself. Anything you say can be used against you in court.

3. Right to a speedy trial: You have the right to a speedy and public trial.

4. Right to confront witnesses: You have the right to confront witnesses against you and to call witnesses in your defense.

5. Right to reasonable bail: You have the right to be released on reasonable bail pending trial, except in certain serious cases.

You also have the following RESPONSIBILITIES:

1. Appear in court: You must appear at all scheduled court appearances. Failure to appear may result in a warrant for your arrest and forfeiture of your bail.

2. Comply with conditions: You must comply with all conditions of your release as set by the court.

3. Remain in the jurisdiction: You must not leave the jurisdiction without permission from the court.

4. Update contact information: You must keep the court and your attorney informed of your current address and phone number.

5. Avoid new charges: You must not commit any new crimes while on release.

Remember, your AI Legal Team is here to help you navigate the legal process and ensure you understand and fulfill your responsibilities.
"""
        case.add_document("rights", "Defendant's Rights and Responsibilities", rights_doc)
    
    def get_case(self, case_id):
        """
        Get a case by ID
        
        Args:
            case_id (str): Case ID
            
        Returns:
            LegalCase: The case if found, None otherwise
        """
        return self.cases.get(case_id)
    
    def get_user_cases(self, user_id):
        """
        Get all cases for a user
        
        Args:
            user_id (str): User ID
            
        Returns:
            list: List of cases for the user
        """
        return [case for case in self.cases.values() if case.user_id == user_id]
    
    def add_note_to_case(self, case_id, note_text, author="AI Legal Team"):
        """
        Add a note to a case
        
        Args:
            case_id (str): Case ID
            note_text (str): Note text
            author (str, optional): Note author
            
        Returns:
            dict: Added note or None if case not found
        """
        case = self.get_case(case_id)
        if not case:
            logger.error(f"Case {case_id} not found")
            return None
        
        note = case.add_note(note_text, author)
        self._save_cases()
        return note
    
    def add_document_to_case(self, case_id, doc_type, title, content, is_template=False):
        """
        Add a document to a case
        
        Args:
            case_id (str): Case ID
            doc_type (str): Document type
            title (str): Document title
            content (str): Document content
            is_template (bool, optional): Whether this is a template
            
        Returns:
            dict: Added document or None if case not found
        """
        case = self.get_case(case_id)
        if not case:
            logger.error(f"Case {case_id} not found")
            return None
        
        document = case.add_document(doc_type, title, content, is_template)
        self._save_cases()
        return document
    
    def add_court_appearance(self, case_id, appearance_date, appearance_type, notes=None):
        """
        Add a court appearance to a case
        
        Args:
            case_id (str): Case ID
            appearance_date (datetime or str): Date and time of appearance
            appearance_type (str): Type of appearance (e.g., "Arraignment", "Preliminary Hearing")
            notes (list, optional): Notes about the appearance
            
        Returns:
            dict: Added appearance or None if case not found
        """
        case = self.get_case(case_id)
        if not case:
            logger.error(f"Case {case_id} not found")
            return None
        
        appearance = case.add_court_appearance(appearance_date, appearance_type, notes)
        
        # Generate court appearance reminder
        if self.config.get("auto_document_generation", True):
            reminder = self.document_generator.generate_court_appearance_reminder(case)
            if reminder:
                case.add_document("court_reminder", f"{appearance_type} Appearance Reminder", reminder)
        
        self._save_cases()
        return appearance
    
    def update_case_status(self, case_id, status):
        """
        Update the status of a case
        
        Args:
            case_id (str): Case ID
            status (str): New status
            
        Returns:
            str: Updated status or None if case not found
        """
        case = self.get_case(case_id)
        if not case:
            logger.error(f"Case {case_id} not found")
            return None
        
        case.update_status(status)
        self._save_cases()
        return status
    
    def generate_legal_document(self, case_id, document_type, context=None):
        """
        Generate a legal document for a case
        
        Args:
            case_id (str): Case ID
            document_type (str): Type of document to generate
            context (dict, optional): Additional context for document generation
            
        Returns:
            dict: Generated document or None if failed
        """
        case = self.get_case(case_id)
        if not case:
            logger.error(f"Case {case_id} not found")
            return None
        
        document_content = None
        document_title = None
        
        # Generate based on document type
        if document_type == "court_reminder":
            document_content = self.document_generator.generate_court_appearance_reminder(case)
            document_title = "Court Appearance Reminder"
        elif document_type == "bail_conditions":
            document_content = self.document_generator.generate_bail_conditions_reminder(case, None)
            document_title = "Bail Conditions and Requirements"
        elif document_type == "motion_to_dismiss":
            arguments = context.get("arguments", []) if context else []
            document_content = self.document_generator.generate_motion_to_dismiss(case, arguments)
            document_title = "Motion to Dismiss"
        else:
            logger.error(f"Unsupported document type: {document_type}")
            return None
        
        if not document_content:
            logger.error(f"Failed to generate {document_type} document")
            return None
        
        # Add the document to the case
        document = case.add_document(document_type, document_title, document_content)
        self._save_cases()
        
        return document
    
    def check_upcoming_court_dates(self, days_ahead=3):
        """
        Check for upcoming court dates and generate reminders
        
        Args:
            days_ahead (int, optional): Number of days ahead to check
            
        Returns:
            list: List of cases with upcoming court dates
        """
        cases_with_dates = []
        
        now = datetime.now()
        reminder_date = now + timedelta(days=days_ahead)
        
        for case in self.cases.values():
            for appearance in case.appearances:
                if appearance["status"] != "scheduled":
                    continue
                
                appearance_date = datetime.fromisoformat(appearance["date"]) if isinstance(appearance["date"], str) else appearance["date"]
                
                # Check if the appearance is within the reminder window
                if now < appearance_date <= reminder_date:
                    # Generate a reminder document if auto-generation is enabled
                    if self.config.get("auto_document_generation", True):
                        reminder = self.document_generator.generate_court_appearance_reminder(case)
                        if reminder:
                            case.add_document("court_reminder", f"Upcoming {appearance['type']} Reminder", reminder)
                            
                            # Add a note about the reminder
                            case.add_note(
                                f"Reminder generated for upcoming {appearance['type']} on {appearance_date.strftime('%B %d, %Y')}. "
                                f"Please review the document for important information."
                            )
                    
                    # Add this case to the list
                    cases_with_dates.append({
                        "case_id": case.case_id,
                        "defendant_name": case.defendant_name,
                        "appearance_type": appearance["type"],
                        "appearance_date": appearance_date.isoformat(),
                        "court_location": case.court_location
                    })
        
        # Save cases if any reminders were generated
        if cases_with_dates and self.config.get("auto_document_generation", True):
            self._save_cases()
        
        return cases_with_dates
    
    def get_legal_resources(self, case_id, query=None, resource_type=None, jurisdiction=None):
        """
        Get legal resources relevant to a case
        
        Args:
            case_id (str): Case ID
            query (str, optional): Search query
            resource_type (str, optional): Type of resource ("case_law", "statutes", "definitions")
            jurisdiction (str, optional): Jurisdiction code
            
        Returns:
            dict: Legal resources
        """
        case = self.get_case(case_id)
        if not case:
            logger.error(f"Case {case_id} not found")
            return {"error": "Case not found"}
        
        # Extract jurisdiction from court location if not provided
        if not jurisdiction:
            court_parts = case.court_location.split(",")
            if len(court_parts) >= 2:
                state_part = court_parts[1].strip()
                jurisdiction = state_part[:2]  # Extract state abbreviation
        
        # If no specific query, extract one from charges
        if not query and case.charges:
            if isinstance(case.charges[0], str):
                query = case.charges[0]
            else:
                query = case.charges[0].get("charge", "bail conditions")
        
        # Default query if none available
        if not query:
            query = "bail conditions"
        
        # Get resources based on type
        resources = {}
        
        if not resource_type or resource_type == "case_law":
            resources["case_law"] = self.legal_library.search_case_law(query, jurisdiction, limit=5)
        
        if not resource_type or resource_type == "statutes":
            resources["statutes"] = self.legal_library.get_bail_statute(jurisdiction or "CA")
        
        if not resource_type or resource_type == "definitions":
            # Extract key terms from query
            terms = ["bail", "arraignment", "pretrial release"]
            resources["definitions"] = [self.legal_library.search_legal_definitions(term) for term in terms]
        
        if not resource_type or resource_type == "procedures":
            court_name = case.court_location.split(",")[0] if "," in case.court_location else case.court_location
            resources["procedures"] = self.legal_library.get_court_procedures(court_name, jurisdiction or "CA")
        
        return resources
    
    def emergency_activation(self, user_id, defendant_info, location, situation_description):
        """
        Emergency activation of the "I'm going to jail" protocol
        
        Args:
            user_id (str): User ID or token holder ID
            defendant_info (dict): Information about the defendant
            location (str): Current location
            situation_description (str): Description of the situation
            
        Returns:
            dict: Activation status and next steps
        """
        # Log the emergency activation
        logger.info(f"Emergency 'I'm going to jail' activation for user {user_id}")
        
        # Record the activation time
        activation_time = datetime.now()
        
        # Create a response with immediate guidance
        response = {
            "activation_id": f"emergency_{int(time.time())}",
            "activation_time": activation_time.isoformat(),
            "status": "activated",
            "user_id": user_id,
            "immediate_guidance": [
                "Remain calm and cooperative with law enforcement",
                "Exercise your right to remain silent",
                "Request to speak with an attorney",
                "Do not consent to searches without a warrant",
                "Inform law enforcement that you have bail assistance through AI CEO"
            ],
            "next_steps": [
                "AI CEO is scanning county databases for booking information",
                "Legal team is being assembled for your case",
                "Bail bond process will initiate once booking is confirmed",
                "GPS tracking will help locate your detention facility",
                "AI legal team will contact the facility once booking is complete"
            ],
            "estimated_response_time": "1-2 hours after booking is completed"
        }
        
        # In a real implementation, this would trigger additional processes:
        # 1. Begin scanning county jail systems for booking information
        # 2. Check token holdings to verify eligibility
        # 3. Prepare bail bond documentation
        # 4. Initialize AI legal team for the case
        
        return response
    
    def get_bail_eligibility(self, user_id, token_data):
        """
        Check if a user is eligible for automatic bail based on token holdings
        
        Args:
            user_id (str): User ID
            token_data (dict): Token holdings data
            
        Returns:
            dict: Eligibility status and details
        """
        # Determine eligibility based on token holdings
        bbgt_tokens = token_data.get("BBGT", {}).get("balance", 0)
        t918_tokens = token_data.get("918T", {}).get("balance", 0)
        
        # Calculate estimated bail coverage (10% of bail total)
        # Example: 1000 BBGT = 1 ETH = $2000 bail coverage
        bbgt_coverage = bbgt_tokens * 0.001 * 20000  # 1 BBGT = 0.001 ETH, 1 ETH = $2000
        t918_coverage = t918_tokens * 0.01 * 20000   # 1 918T = 0.01 ETH, 1 ETH = $2000
        
        total_coverage = bbgt_coverage + t918_coverage
        
        # Calculate eligibility tiers
        eligibility = {
            "user_id": user_id,
            "total_tokens": {
                "BBGT": bbgt_tokens,
                "918T": t918_tokens
            },
            "coverage_estimate": {
                "amount_usd": total_coverage,
                "max_bail_amount": total_coverage * 10  # 10x because coverage is 10% of bail
            },
            "eligibility_tier": "None"
        }
        
        # Determine tier based on coverage
        if total_coverage >= 50000:
            eligibility["eligibility_tier"] = "Platinum"
            eligibility["benefits"] = [
                "Automatic bail up to $500,000",
                "Priority processing within 30 minutes",
                "Full legal team with specialized attorneys",
                "Premium monitoring system",
                "Expedited release processing"
            ]
        elif total_coverage >= 25000:
            eligibility["eligibility_tier"] = "Gold"
            eligibility["benefits"] = [
                "Automatic bail up to $250,000",
                "Fast processing within 1 hour",
                "Full legal team",
                "Advanced monitoring system",
                "Priority release processing"
            ]
        elif total_coverage >= 10000:
            eligibility["eligibility_tier"] = "Silver"
            eligibility["benefits"] = [
                "Automatic bail up to $100,000",
                "Processing within 2 hours",
                "Standard legal team",
                "Standard monitoring system",
                "Standard release processing"
            ]
        elif total_coverage >= 5000:
            eligibility["eligibility_tier"] = "Bronze"
            eligibility["benefits"] = [
                "Automatic bail up to $50,000",
                "Processing within 3 hours",
                "Basic legal team",
                "Basic monitoring system",
                "Basic release processing"
            ]
        else:
            eligibility["eligibility_tier"] = "Not Eligible"
            eligibility["message"] = "Insufficient token holdings for automatic bail. Minimum coverage requirement: $5,000."
            eligibility["recommendation"] = "Consider acquiring more BBGT or 918T tokens to access automatic bail services."
        
        return eligibility