"""
Symptom Prediction Engine
Uses comparative epidemiological analysis to predict symptom patterns for emerging viruses
Based on the 3M approach: Monitoring-Modelling-Managing
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from .historical_data import HISTORICAL_PANDEMICS, PARAMETER_RANGES

class SymptomPredictor:
    """
    Predicts probable symptom patterns for emerging viruses based on 
    comparative analysis with historical pandemic data
    """
    
    def __init__(self):
        self.historical_data = HISTORICAL_PANDEMICS
        self.feature_weights = {
            'r0': 0.25,
            'incubation_period': 0.15,
            'case_fatality_rate': 0.20,
            'serial_interval': 0.10,
            'hospitalization_rate': 0.15,
            'asymptomatic_rate': 0.15
        }
    
    def calculate_similarity(self, new_virus_params: Dict, historical_pandemic: str) -> float:
        """
        Calculate similarity score between new virus and historical pandemic
        Uses weighted Euclidean distance on normalized parameters
        """
        historical = self.historical_data[historical_pandemic]['epidemiology']
        
        # Normalize and calculate weighted distance
        total_distance = 0.0
        total_weight = 0.0
        
        for param, weight in self.feature_weights.items():
            if param in new_virus_params and param in historical:
                # Normalize based on parameter ranges
                new_val = new_virus_params[param]
                hist_val = historical[param]
                
                # Get normalization range
                if param == 'r0':
                    max_val = 10.0
                elif param == 'incubation_period' or param == 'serial_interval':
                    max_val = 30.0
                elif param == 'case_fatality_rate' or param == 'hospitalization_rate' or param == 'asymptomatic_rate':
                    max_val = 100.0
                else:
                    max_val = max(new_val, hist_val) if max(new_val, hist_val) > 0 else 1.0
                
                # Normalized distance
                norm_new = new_val / max_val
                norm_hist = hist_val / max_val
                distance = abs(norm_new - norm_hist)
                
                total_distance += weight * (distance ** 2)
                total_weight += weight
        
        # Convert distance to similarity (0-100%)
        if total_weight > 0:
            normalized_distance = np.sqrt(total_distance / total_weight)
            similarity = max(0, 100 * (1 - normalized_distance))
        else:
            similarity = 0.0
        
        return similarity
    
    def find_similar_pandemics(self, new_virus_params: Dict, top_n: int = 3) -> List[Tuple[str, float]]:
        """
        Find the most similar historical pandemics to the new virus
        Returns list of (pandemic_name, similarity_score) tuples
        """
        similarities = []
        
        for pandemic_name in self.historical_data.keys():
            similarity = self.calculate_similarity(new_virus_params, pandemic_name)
            similarities.append((pandemic_name, similarity))
        
        # Sort by similarity (descending) and return top N
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]
    
    def predict_symptom_profile(self, new_virus_params: Dict, top_n: int = 3) -> Dict:
        """
        Predict probable symptom profile based on similar historical pandemics
        Uses weighted average based on similarity scores
        """
        similar_pandemics = self.find_similar_pandemics(new_virus_params, top_n)
        
        # Collect all symptoms from similar pandemics with weights
        symptom_aggregator = {}
        total_similarity = sum([sim for _, sim in similar_pandemics])
        
        for pandemic_name, similarity in similar_pandemics:
            weight = similarity / total_similarity if total_similarity > 0 else 1.0 / len(similar_pandemics)
            pandemic_data = self.historical_data[pandemic_name]
            
            # Aggregate primary symptoms
            for symptom in pandemic_data['symptoms']['primary']:
                name = symptom['name']
                if name not in symptom_aggregator:
                    symptom_aggregator[name] = {
                        'prevalence': 0.0,
                        'severity': symptom['severity'],
                        'onset_day': 0.0,
                        'count': 0,
                        'category': 'primary'
                    }
                symptom_aggregator[name]['prevalence'] += symptom['prevalence'] * weight
                symptom_aggregator[name]['onset_day'] += symptom['onset_day'] * weight
                symptom_aggregator[name]['count'] += 1
            
            # Aggregate secondary symptoms
            for symptom in pandemic_data['symptoms']['secondary']:
                name = symptom['name']
                if name not in symptom_aggregator:
                    symptom_aggregator[name] = {
                        'prevalence': 0.0,
                        'severity': symptom['severity'],
                        'onset_day': 0.0,
                        'count': 0,
                        'category': 'secondary'
                    }
                symptom_aggregator[name]['prevalence'] += symptom['prevalence'] * weight
                symptom_aggregator[name]['onset_day'] += symptom['onset_day'] * weight
                symptom_aggregator[name]['count'] += 1
        
        # Normalize and sort symptoms
        predicted_symptoms = {
            'primary': [],
            'secondary': [],
            'severe_complications': []
        }
        
        for name, data in symptom_aggregator.items():
            symptom_entry = {
                'name': name,
                'predicted_prevalence': round(data['prevalence'], 1),
                'severity': data['severity'],
                'predicted_onset_day': round(data['onset_day'], 1),
                'confidence': round(min(100, (data['count'] / len(similar_pandemics)) * 100), 1)
            }
            
            if data['category'] == 'primary' and data['prevalence'] > 30:
                predicted_symptoms['primary'].append(symptom_entry)
            elif data['prevalence'] > 10:
                predicted_symptoms['secondary'].append(symptom_entry)
        
        # Sort by prevalence
        predicted_symptoms['primary'].sort(key=lambda x: x['predicted_prevalence'], reverse=True)
        predicted_symptoms['secondary'].sort(key=lambda x: x['predicted_prevalence'], reverse=True)
        
        # Predict severe complications based on CFR
        cfr = new_virus_params.get('case_fatality_rate', 1.0)
        if cfr > 10:  # High mortality
            predicted_symptoms['severe_complications'] = [
                {'name': 'Multi-organ Failure', 'risk': 'high', 'estimated_prevalence': round(cfr * 1.5, 1)},
                {'name': 'ARDS', 'risk': 'high', 'estimated_prevalence': round(cfr * 2.0, 1)},
                {'name': 'Septic Shock', 'risk': 'high', 'estimated_prevalence': round(cfr * 1.2, 1)}
            ]
        elif cfr > 2:  # Moderate mortality
            predicted_symptoms['severe_complications'] = [
                {'name': 'Pneumonia', 'risk': 'moderate', 'estimated_prevalence': round(cfr * 5.0, 1)},
                {'name': 'ARDS', 'risk': 'moderate', 'estimated_prevalence': round(cfr * 2.5, 1)}
            ]
        else:  # Low mortality
            predicted_symptoms['severe_complications'] = [
                {'name': 'Pneumonia', 'risk': 'low', 'estimated_prevalence': round(cfr * 8.0, 1)},
                {'name': 'Bronchitis', 'risk': 'low', 'estimated_prevalence': round(cfr * 10.0, 1)}
            ]
        
        return {
            'predicted_symptoms': predicted_symptoms,
            'similar_pandemics': similar_pandemics,
            'confidence_score': round(sum([sim for _, sim in similar_pandemics]) / len(similar_pandemics), 1)
        }
    
    def predict_age_impact(self, new_virus_params: Dict, top_n: int = 3) -> Dict:
        """
        Predict age-specific impact based on similar pandemics
        """
        similar_pandemics = self.find_similar_pandemics(new_virus_params, top_n)
        
        age_groups = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
        age_predictions = {}
        
        total_similarity = sum([sim for _, sim in similar_pandemics])
        
        for age_group in age_groups:
            infection_rate = 0.0
            severity_score = 0.0
            cfr = 0.0
            
            for pandemic_name, similarity in similar_pandemics:
                weight = similarity / total_similarity if total_similarity > 0 else 1.0 / len(similar_pandemics)
                age_data = self.historical_data[pandemic_name]['age_impact'].get(age_group, {})
                
                infection_rate += age_data.get('infection_rate', 1.0) * weight
                severity_score += age_data.get('severity_score', 1.0) * weight
                cfr += age_data.get('cfr', 1.0) * weight
            
            age_predictions[age_group] = {
                'predicted_infection_rate': round(infection_rate, 2),
                'predicted_severity_score': round(severity_score, 2),
                'predicted_cfr': round(cfr, 2)
            }
        
        return age_predictions
    
    def generate_prediction_report(self, new_virus_params: Dict, virus_name: str = "Unknown Virus") -> Dict:
        """
        Generate comprehensive prediction report
        """
        # Get symptom predictions
        symptom_prediction = self.predict_symptom_profile(new_virus_params)
        
        # Get age impact predictions
        age_impact = self.predict_age_impact(new_virus_params)
        
        # Categorize virus characteristics
        r0 = new_virus_params.get('r0', 2.0)
        cfr = new_virus_params.get('case_fatality_rate', 1.0)
        
        if r0 < 1.5:
            transmissibility_category = "Low"
        elif r0 < 2.5:
            transmissibility_category = "Moderate"
        elif r0 < 4.0:
            transmissibility_category = "High"
        else:
            transmissibility_category = "Very High"
        
        if cfr < 0.5:
            severity_category = "Low"
        elif cfr < 2.0:
            severity_category = "Moderate"
        elif cfr < 10.0:
            severity_category = "High"
        else:
            severity_category = "Very High"
        
        # Generate insights
        insights = self._generate_insights(new_virus_params, symptom_prediction)
        
        return {
            'virus_name': virus_name,
            'input_parameters': new_virus_params,
            'transmissibility_category': transmissibility_category,
            'severity_category': severity_category,
            'symptom_predictions': symptom_prediction['predicted_symptoms'],
            'age_impact_predictions': age_impact,
            'similar_historical_pandemics': symptom_prediction['similar_pandemics'],
            'overall_confidence': symptom_prediction['confidence_score'],
            'insights': insights,
            'disclaimer': "These predictions are based on comparative analysis with historical data and should be used for preparedness planning, not clinical diagnosis."
        }
    
    def _generate_insights(self, params: Dict, symptom_data: Dict) -> List[str]:
        """
        Generate actionable insights from prediction
        """
        insights = []
        
        r0 = params.get('r0', 2.0)
        cfr = params.get('case_fatality_rate', 1.0)
        
        # Transmissibility insights
        if r0 > 2.5:
            insights.append(f"⚠️ High transmissibility (R₀={r0:.1f}) suggests rapid spread - early intervention critical")
        
        # Severity insights
        if cfr > 5.0:
            insights.append(f"🏥 High case fatality rate ({cfr:.1f}%) indicates need for extensive healthcare preparedness")
        
        # Symptom pattern insights
        primary_count = len(symptom_data['predicted_symptoms']['primary'])
        if primary_count > 5:
            insights.append(f"📊 Complex symptom profile ({primary_count} primary symptoms) may complicate early detection")
        
        # Similar pandemic insights
        top_match = symptom_data['similar_pandemics'][0]
        insights.append(f"🔍 Closest match: {top_match[0]} ({top_match[1]:.0f}% similarity) - review historical response strategies")
        
        # Confidence note
        if symptom_data['confidence_score'] < 60:
            insights.append("⚡ Moderate confidence - limited historical matches, monitor closely for emerging patterns")
        
        return insights
