"""
Career Mapping AI - Second AI system for career recommendations.
Runs weekly after StudyBuddy AI finishes processing.
"""
from typing import List, Dict
from datetime import datetime
from extended_models import (
    UserTier, StudyBuddyReport, StudentInterests, CareerPath,
    SkillRating, CareerMappingReport, GradeLevel
)


class CareerMappingAI:
    """
    AI #2 - Data Analytics + Career Mapping AI
    
    Runs once per week after StudyBuddy finishes processing.
    Matches student strengths/interests to career paths.
    """
    
    # Career database (simplified for prototype)
    CAREER_DATABASE = {
        "software_engineer": {
            "title": "Software Engineer",
            "required_skills": {
                "analytical_skills": 4.5,
                "tech_affinity": 5.0,
                "problem_solving": 4.5,
                "creativity": 3.5,
                "people_skills": 2.5
            },
            "related_subjects": ["mathematics", "algebra", "physics", "computer science"],
            "zimbabwe_examples": [
                "Developers at Econet Wireless Zimbabwe",
                "Tech startups in Harare Innovation Hub",
                "Software teams at Old Mutual Zimbabwe"
            ]
        },
        "accountant": {
            "title": "Accountant",
            "required_skills": {
                "analytical_skills": 5.0,
                "tech_affinity": 3.0,
                "problem_solving": 4.0,
                "creativity": 2.0,
                "people_skills": 3.0
            },
            "related_subjects": ["mathematics", "accounting", "economics"],
            "zimbabwe_examples": [
                "Chartered Accountants at Deloitte Zimbabwe",
                "Financial analysts at banks",
                "Government accountants"
            ]
        },
        "teacher": {
            "title": "Teacher/Educator",
            "required_skills": {
                "analytical_skills": 3.5,
                "tech_affinity": 2.5,
                "problem_solving": 3.5,
                "creativity": 4.0,
                "people_skills": 5.0
            },
            "related_subjects": ["all"],
            "zimbabwe_examples": [
                "Teachers at government schools",
                "Private school educators",
                "University lecturers"
            ]
        },
        "data_scientist": {
            "title": "Data Scientist",
            "required_skills": {
                "analytical_skills": 5.0,
                "tech_affinity": 4.5,
                "problem_solving": 5.0,
                "creativity": 3.5,
                "people_skills": 2.5
            },
            "related_subjects": ["mathematics", "statistics", "computer science"],
            "zimbabwe_examples": [
                "Data analysts at telecom companies",
                "Business intelligence at banks",
                "Research institutions"
            ]
        },
        "nurse": {
            "title": "Nurse/Healthcare Worker",
            "required_skills": {
                "analytical_skills": 3.0,
                "tech_affinity": 2.0,
                "problem_solving": 4.0,
                "creativity": 2.5,
                "people_skills": 5.0
            },
            "related_subjects": ["biology", "chemistry", "health science"],
            "zimbabwe_examples": [
                "Nurses at Parirenyatwa Hospital",
                "Community health workers",
                "Private clinic staff"
            ]
        },
        "engineer": {
            "title": "Engineer (Civil/Mechanical)",
            "required_skills": {
                "analytical_skills": 4.5,
                "tech_affinity": 4.0,
                "problem_solving": 5.0,
                "creativity": 4.0,
                "people_skills": 3.0
            },
            "related_subjects": ["mathematics", "physics", "design technology"],
            "zimbabwe_examples": [
                "Engineers at ZINWA",
                "Construction project managers",
                "Mining engineers"
            ]
        },
        "entrepreneur": {
            "title": "Entrepreneur/Business Owner",
            "required_skills": {
                "analytical_skills": 3.5,
                "tech_affinity": 3.0,
                "problem_solving": 4.5,
                "creativity": 5.0,
                "people_skills": 4.5
            },
            "related_subjects": ["business studies", "economics", "accounting"],
            "zimbabwe_examples": [
                "SME owners in Bulawayo",
                "Agribusiness entrepreneurs",
                "Tech startup founders"
            ]
        }
    }
    
    def __init__(self):
        """Initialize Career Mapping AI."""
        pass
    
    def generate_career_recommendations(
        self,
        student_id: str,
        studybuddy_report: StudyBuddyReport,
        interests: StudentInterests,
        tier: UserTier = UserTier.FREE
    ) -> CareerMappingReport:
        """
        Generate career recommendations based on performance and interests.
        
        Args:
            student_id: Student identifier
            studybuddy_report: Output from StudyBuddy AI
            interests: Student's interests and preferences
            tier: User subscription tier
            
        Returns:
            CareerMappingReport with career recommendations
        """
        report = CareerMappingReport(
            student_id=student_id,
            report_date=datetime.now(),
            tier=tier
        )
        
        # Calculate skill ratings from performance
        skill_ratings = self._calculate_skill_ratings(
            studybuddy_report, interests
        )
        report.skill_ratings = skill_ratings
        
        # Match careers
        career_matches = self._match_careers(
            skill_ratings, interests, studybuddy_report
        )
        
        # Sort by match score and take top 5
        career_matches.sort(key=lambda c: c.match_score, reverse=True)
        report.career_paths = career_matches[:5]
        
        # Premium features
        if tier == UserTier.PREMIUM:
            report.skill_gap_analysis = self._generate_skill_gap_analysis(
                skill_ratings, report.career_paths
            )
            report.self_improvement_plan = self._create_improvement_plan(
                studybuddy_report, interests
            )
            report.career_clusters = self._identify_career_clusters(
                report.career_paths
            )
        
        return report
    
    def _calculate_skill_ratings(
        self,
        studybuddy_report: StudyBuddyReport,
        interests: StudentInterests
    ) -> List[SkillRating]:
        """Calculate skill ratings based on performance and interests."""
        skill_ratings = []
        
        # Analytical skills (from math/science performance)
        analytical_score = self._calculate_analytical_score(studybuddy_report)
        skill_ratings.append(SkillRating(
            skill_name="Analytical Skills",
            rating=analytical_score,
            evidence=f"Based on performance in math and science subjects"
        ))
        
        # Problem-solving (from overall performance and difficulty progression)
        problem_solving_score = self._calculate_problem_solving_score(
            studybuddy_report
        )
        skill_ratings.append(SkillRating(
            skill_name="Problem Solving",
            rating=problem_solving_score,
            evidence=f"Based on ability to tackle different difficulty levels"
        ))
        
        # Tech affinity (from related subjects and interests)
        tech_score = self._calculate_tech_affinity(studybuddy_report, interests)
        skill_ratings.append(SkillRating(
            skill_name="Tech Affinity",
            rating=tech_score,
            evidence=f"Based on interest and performance in tech-related subjects"
        ))
        
        # Creativity (from diverse subject engagement)
        creativity_score = self._calculate_creativity_score(
            studybuddy_report, interests
        )
        skill_ratings.append(SkillRating(
            skill_name="Creativity",
            rating=creativity_score,
            evidence=f"Based on diversity of subject engagement"
        ))
        
        # People skills (from social subjects and interests)
        people_score = self._calculate_people_skills(interests)
        skill_ratings.append(SkillRating(
            skill_name="People Skills",
            rating=people_score,
            evidence=f"Based on interests in social and collaborative areas"
        ))
        
        return skill_ratings
    
    def _calculate_analytical_score(
        self, studybuddy_report: StudyBuddyReport
    ) -> float:
        """Calculate analytical skills rating (0-5)."""
        # Look for math/science subjects
        analytical_subjects = ["mathematics", "algebra", "physics", "chemistry", "statistics"]
        
        total_strength = 0.0
        count = 0
        
        for subject_strength in studybuddy_report.subject_strengths:
            if any(subj in subject_strength.subject.lower() for subj in analytical_subjects):
                total_strength += subject_strength.strength_score
                count += 1
        
        if count == 0:
            return 2.5  # Default middle rating
        
        avg_strength = total_strength / count
        # Convert 0-100 to 0-5
        return (avg_strength / 100) * 5
    
    def _calculate_problem_solving_score(
        self, studybuddy_report: StudyBuddyReport
    ) -> float:
        """Calculate problem-solving rating (0-5)."""
        # Based on overall confidence and trend
        confidence = studybuddy_report.overall_confidence
        
        # Bonus for improving trend
        trend_bonus = 0.0
        if studybuddy_report.overall_trend.name == "IMPROVING":
            trend_bonus = 0.5
        elif studybuddy_report.overall_trend.name == "DECLINING":
            trend_bonus = -0.5
        
        base_score = (confidence / 100) * 5
        return min(5.0, max(0.0, base_score + trend_bonus))
    
    def _calculate_tech_affinity(
        self, studybuddy_report: StudyBuddyReport, interests: StudentInterests
    ) -> float:
        """Calculate tech affinity rating (0-5)."""
        tech_subjects = ["computer science", "programming", "ict", "technology"]
        
        score = 2.5  # Default
        
        # Check subject performance
        for subject_strength in studybuddy_report.subject_strengths:
            if any(tech in subject_strength.subject.lower() for tech in tech_subjects):
                score = (subject_strength.strength_score / 100) * 5
                break
        
        # Check interests
        tech_interests = ["computers", "coding", "technology", "programming", "gaming"]
        if any(tech in " ".join(interests.interests).lower() for tech in tech_interests):
            score = min(5.0, score + 1.0)
        
        return score
    
    def _calculate_creativity_score(
        self, studybuddy_report: StudyBuddyReport, interests: StudentInterests
    ) -> float:
        """Calculate creativity rating (0-5)."""
        # Diversity of subjects engaged with
        num_subjects = len(studybuddy_report.subject_strengths)
        
        base_score = min(4.0, num_subjects * 0.5)
        
        # Creative interests
        creative_interests = ["art", "music", "design", "writing", "creative"]
        if any(c in " ".join(interests.interests).lower() for c in creative_interests):
            base_score = min(5.0, base_score + 1.5)
        
        return base_score
    
    def _calculate_people_skills(self, interests: StudentInterests) -> float:
        """Calculate people skills rating (0-5)."""
        people_interests = [
            "teaching", "helping", "social", "leadership", "community",
            "teamwork", "sports", "communication"
        ]
        
        score = 2.5  # Default
        
        interest_text = " ".join(interests.interests).lower()
        matches = sum(1 for p in people_interests if p in interest_text)
        
        # More matches = higher people skills
        score = min(5.0, 2.5 + (matches * 0.5))
        
        return score
    
    def _match_careers(
        self,
        skill_ratings: List[SkillRating],
        interests: StudentInterests,
        studybuddy_report: StudyBuddyReport
    ) -> List[CareerPath]:
        """Match student profile to careers."""
        career_paths = []
        
        # Convert skill ratings to dict
        skills_dict = {
            sr.skill_name.lower().replace(" ", "_"): sr.rating 
            for sr in skill_ratings
        }
        
        for career_id, career_data in self.CAREER_DATABASE.items():
            match_score = self._calculate_career_match(
                skills_dict, career_data, interests, studybuddy_report
            )
            
            career_path = CareerPath(
                career_id=career_id,
                title=career_data["title"],
                match_score=match_score,
                problem_solving=skills_dict.get("problem_solving", 0),
                creativity=skills_dict.get("creativity", 0),
                people_skills=skills_dict.get("people_skills", 0),
                tech_affinity=skills_dict.get("tech_affinity", 0),
                analytical_skills=skills_dict.get("analytical_skills", 0),
                why_matched=self._explain_match(career_data, skills_dict, interests),
                skills_needed=self._get_skills_needed(career_data),
                zimbabwe_examples=career_data.get("zimbabwe_examples", []),
                recommended_articles=self._get_resources(career_id, "articles"),
                recommended_videos=self._get_resources(career_id, "videos"),
                reading_list=self._get_resources(career_id, "books")
            )
            
            career_paths.append(career_path)
        
        return career_paths
    
    def _calculate_career_match(
        self,
        skills_dict: Dict[str, float],
        career_data: Dict,
        interests: StudentInterests,
        studybuddy_report: StudyBuddyReport
    ) -> float:
        """Calculate match score (0-100) for a career."""
        required_skills = career_data["required_skills"]
        
        # Calculate skill match
        skill_matches = []
        for skill_name, required_level in required_skills.items():
            student_level = skills_dict.get(skill_name, 2.5)
            # How close is student to required level?
            match = 100 - (abs(required_level - student_level) * 20)
            skill_matches.append(max(0, match))
        
        avg_skill_match = sum(skill_matches) / len(skill_matches)
        
        # Subject match bonus
        subject_bonus = 0
        related_subjects = career_data.get("related_subjects", [])
        if "all" not in related_subjects:
            for subject_strength in studybuddy_report.subject_strengths:
                if any(subj in subject_strength.subject.lower() for subj in related_subjects):
                    if subject_strength.strength_score > 70:
                        subject_bonus += 10
        
        # Interest match bonus
        interest_bonus = 0
        career_title_lower = career_data["title"].lower()
        interest_text = " ".join(interests.interests).lower()
        if any(word in interest_text for word in career_title_lower.split()):
            interest_bonus = 15
        
        total_score = min(100, avg_skill_match + subject_bonus + interest_bonus)
        return total_score
    
    def _explain_match(
        self, career_data: Dict, skills_dict: Dict, interests: StudentInterests
    ) -> str:
        """Explain why this career matches the student."""
        title = career_data["title"]
        
        # Find top 2 matching skills
        required = career_data["required_skills"]
        matches = []
        for skill, req_level in required.items():
            student_level = skills_dict.get(skill, 0)
            if student_level >= req_level * 0.8:  # Within 80% of required
                skill_display = skill.replace("_", " ").title()
                matches.append(skill_display)
        
        if matches:
            skills_text = " and ".join(matches[:2])
            return f"Your strong {skills_text} align well with {title} requirements."
        else:
            return f"{title} could be a good fit with some skill development."
    
    def _get_skills_needed(self, career_data: Dict) -> List[str]:
        """Get list of skills needed for career."""
        skills = []
        for skill, level in career_data["required_skills"].items():
            skill_display = skill.replace("_", " ").title()
            skills.append(f"{skill_display} (Level {level:.1f}/5)")
        return skills
    
    def _get_resources(self, career_id: str, resource_type: str) -> List[str]:
        """Get educational resources for a career."""
        # Simplified resource recommendations
        resources = {
            "articles": [
                f"Introduction to {career_id.replace('_', ' ').title()}",
                f"Career Guide: {career_id.replace('_', ' ').title()} in Zimbabwe"
            ],
            "videos": [
                f"Day in the Life of a {career_id.replace('_', ' ').title()}",
                f"Skills needed for {career_id.replace('_', ' ').title()}"
            ],
            "books": [
                f"Guide to {career_id.replace('_', ' ').title()}",
                f"Success in {career_id.replace('_', ' ').title()}"
            ]
        }
        return resources.get(resource_type, [])
    
    def _generate_skill_gap_analysis(
        self, skill_ratings: List[SkillRating], career_paths: List[CareerPath]
    ) -> str:
        """Generate detailed skill gap analysis (Premium only)."""
        if not career_paths:
            return "No career matches found."
        
        top_career = career_paths[0]
        
        analysis = f"For {top_career.title}:\n\n"
        
        # Analyze each skill
        skills_dict = {sr.skill_name.lower().replace(" ", "_"): sr.rating for sr in skill_ratings}
        
        gaps = []
        strengths = []
        
        for skill_name in ["analytical_skills", "problem_solving", "creativity", "people_skills", "tech_affinity"]:
            student_level = skills_dict.get(skill_name, 0)
            required_level = getattr(top_career, skill_name, 0)
            
            gap = required_level - student_level
            skill_display = skill_name.replace("_", " ").title()
            
            if gap > 1.0:
                gaps.append(f"- {skill_display}: Need to improve by {gap:.1f} points")
            elif gap > 0:
                gaps.append(f"- {skill_display}: Close, improve by {gap:.1f} points")
            else:
                strengths.append(f"- {skill_display}: Already at required level!")
        
        if strengths:
            analysis += "Strengths:\n" + "\n".join(strengths) + "\n\n"
        
        if gaps:
            analysis += "Areas to develop:\n" + "\n".join(gaps)
        else:
            analysis += "You meet all skill requirements!"
        
        return analysis
    
    def _create_improvement_plan(
        self, studybuddy_report: StudyBuddyReport, interests: StudentInterests
    ) -> str:
        """Create self-improvement plan (Premium only)."""
        plan = "Your Personalized Improvement Plan:\n\n"
        
        # Focus on weakest subjects
        weak_subjects = [
            s for s in studybuddy_report.subject_strengths
            if s.weakness_score > 50
        ]
        
        if weak_subjects:
            plan += "Week 1-2: Focus on strengthening weak areas:\n"
            for subject in weak_subjects[:2]:
                plan += f"- Study {subject.subject} for 30 minutes daily\n"
            plan += "\n"
        
        plan += "Week 3-4: Build on strengths:\n"
        strong_subjects = [
            s for s in studybuddy_report.subject_strengths
            if s.strength_score > 70
        ]
        for subject in strong_subjects[:2]:
            plan += f"- Advance in {subject.subject} with challenging problems\n"
        
        return plan
    
    def _identify_career_clusters(
        self, career_paths: List[CareerPath]
    ) -> List[str]:
        """Identify career clusters (Premium only)."""
        # Group similar careers
        clusters = set()
        
        for career in career_paths:
            title_lower = career.title.lower()
            if "engineer" in title_lower or "tech" in title_lower:
                clusters.add("Technology & Engineering")
            elif "teacher" in title_lower or "educat" in title_lower:
                clusters.add("Education & Training")
            elif "account" in title_lower or "business" in title_lower:
                clusters.add("Business & Finance")
            elif "health" in title_lower or "nurse" in title_lower:
                clusters.add("Healthcare")
            else:
                clusters.add("Professional Services")
        
        return list(clusters)
