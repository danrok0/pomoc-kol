from typing import Dict, Any, Optional
from datetime import datetime

class WeatherUtils:
    """Klasa narzędzi do przetwarzania danych pogodowych."""

    @staticmethod
    def format_weather_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formatuje dane pogodowe do bardziej czytelnej postaci."""
        if not weather_data:
            return {}
            
        return {
            'temperatura': {
                'min': round(weather_data.get('temperature_min', 0), 1),
                'max': round(weather_data.get('temperature_max', 0), 1),
                'średnia': round(weather_data.get('temperature', 0), 1)
            },
            'opady': round(weather_data.get('precipitation', 0), 1),
            'zachmurzenie': round(weather_data.get('cloud_cover', 0), 1),
            'godziny_słoneczne': round(weather_data.get('sunshine_hours', 0), 1),
            'prędkość_wiatru': round(weather_data.get('wind_speed', 0), 1)
        }
    
    @staticmethod
    def is_weather_suitable(weather_data: Dict[str, Any], 
                          max_precipitation: float,
                          min_temperature: float,
                          max_temperature: float) -> bool:
        """Sprawdza czy warunki pogodowe są odpowiednie dla wycieczki."""
        if not weather_data:
            return False
            
        avg_temp = weather_data.get('temperature', 0)
        precipitation = weather_data.get('precipitation', 0)
        
        return (min_temperature <= avg_temp <= max_temperature and 
                precipitation <= max_precipitation)
    
    @staticmethod
    def get_weather_summary(weather_data: Dict[str, Any]) -> str:
        """Tworzy podsumowanie warunków pogodowych."""
        if not weather_data:
            return "Brak danych pogodowych"
            
        temp_min = weather_data.get('temperature_min', 0)
        temp_max = weather_data.get('temperature_max', 0)
        precipitation = weather_data.get('precipitation', 0)
        cloud_cover = weather_data.get('cloud_cover', 0)
        sunshine = weather_data.get('sunshine_hours', 0)
        
        return (f"Temperatura: {temp_min:.1f}°C - {temp_max:.1f}°C\n"
                f"Opady: {precipitation:.1f} mm\n"
                f"Zachmurzenie: {cloud_cover:.1f}%\n"
                f"Godziny słoneczne: {sunshine:.1f} h")
    
    @staticmethod
    def get_weather_condition(weather_data: Dict[str, Any]) -> str:
        """Określa ogólny stan pogody."""
        if not weather_data:
            return "nieznany"
            
        precipitation = weather_data.get('precipitation', 0)
        cloud_cover = weather_data.get('cloud_cover', 0)
        sunshine = weather_data.get('sunshine_hours', 0)
        
        if precipitation > 5:
            return "deszczowo"
        elif cloud_cover > 70:
            return "pochmurno"
        elif sunshine > 6:
            return "słonecznie"
        else:
            return "umiarkowanie"
    @staticmethod
    def calculate_hiking_comfort(weather_data: Dict[str, Any]) -> float:
        """
        Oblicza indeks komfortu dla wędrówek (0-100) na podstawie warunków pogodowych.
        
        Parametry brane pod uwagę:
        - Temperatura (optymalna: 15-20°C)
        - Opady (brak opadów najlepszy)
        - Zachmurzenie (lekkie do umiarkowanego optymalne)
        """
        if not weather_data:
            return 50.0  # Wartość domyślna przy braku danych
            
        # Oblicz średnią temperaturę z min i max jeśli dostępne
        temp_min = weather_data.get('temperature_min')
        temp_max = weather_data.get('temperature_max')
        
        if temp_min is not None and temp_max is not None:
            temp = (temp_min + temp_max) / 2
        else:
            temp = weather_data.get('temperature', 20)
            
        # Temperatura (waga: 40%)
        # Zmniejszony optymalny zakres i bardziej surowe kary
        if 15 <= temp <= 18:  # Zmniejszony górny próg z 20°C do 18°C
            temp_score = 100
        elif temp < 15:
            temp_score = max(0, 100 - abs(15 - temp) * 15)  # Zwiększona kara z 12 do 15 punktów za każdy stopień poniżej 15°C
        else:
            temp_score = max(0, 100 - abs(temp - 18) * 18)  # Zwiększona kara z 15 do 18 punktów za każdy stopień powyżej 18°C
            
        # Opady (waga: 35%)
        # Bardziej surowe kary za opady
        precip = weather_data.get('precipitation', 0)
        precip_score = max(0, 100 - (precip * 40))  # Zwiększona kara z 30 do 40 punktów za każdy mm opadów
            
        # Zachmurzenie (waga: 25%)
        # Bardziej surowa ocena zachmurzenia
        cloud = weather_data.get('cloud_cover', 50)
        if cloud < 20:
            cloud_score = 80  # Prawie bezchmurnie (nie idealne - może być za gorąco)
        elif 20 <= cloud <= 40:
            cloud_score = 100  # Lekkie zachmurzenie - idealne
        elif cloud < 60:
            cloud_score = 60  # Umiarkowane zachmurzenie
        else:
            cloud_score = max(0, 100 - ((cloud - 60) * 2))  # Liniowy spadek punktów dla dużego zachmurzenia
            
        # Oblicz końcowy wynik (ważona średnia)
        comfort_index = (
            temp_score * 0.4 +  # Temperatura ma największy wpływ
            precip_score * 0.35 +  # Opady mają duży wpływ
            cloud_score * 0.25  # Zachmurzenie ma najmniejszy wpływ
        )
            
        return round(comfort_index, 1)
    
    @staticmethod
    def analyze_best_periods(weather_data: Dict[str, Dict[str, Any]], trail_type: str = None) -> Dict[str, Any]:
        """
        Analizuje dane pogodowe aby określić najlepsze okresy dla szlaku.
        
        Args:
            weather_data: Słownik danych pogodowych (data -> warunki)
            trail_type: Typ szlaku ('górski', 'leśny', 'nizinny', 'miejski')
            
        Returns:
            Dict zawierający:
            - best_dates: Lista dat z najlepszymi warunkami
            - average_comfort: Średni indeks komfortu
            - recommendations: Zalecenia dotyczące najlepszej pory roku
        """
        if not weather_data:
            return {
                "best_dates": [],
                "average_comfort": 0.0,
                "recommendations": "Brak wystarczających danych pogodowych"
            }

        # Oblicz indeks komfortu dla każdej daty
        comfort_scores = {}
        for date, conditions in weather_data.items():
            comfort = WeatherUtils.calculate_hiking_comfort(conditions)
            
            # Dodatkowe modyfikatory w zależności od typu szlaku
            if trail_type:
                if trail_type == 'górski':
                    # Dla szlaków górskich, większa waga na wiatr i opady
                    wind_penalty = max(0, (conditions.get('wind_speed', 0) - 15) * 2)
                    comfort = max(0, comfort - wind_penalty)
                elif trail_type == 'leśny':
                    # Dla szlaków leśnych, mniejsza waga na zachmurzenie
                    comfort = min(100, comfort + 10)
            
            comfort_scores[date] = comfort

        # Znajdź najlepsze daty (comfort > 70)
        best_dates = [date for date, score in comfort_scores.items() if score > 70]
        best_dates.sort(reverse=True)  # Sortuj od najnowszej daty

        # Oblicz średni indeks komfortu
        avg_comfort = sum(comfort_scores.values()) / len(comfort_scores) if comfort_scores else 0.0

        # Przeanalizuj sezonowość
        seasons = {
            'wiosna': [], 'lato': [], 'jesień': [], 'zima': []
        }
        
        for date in weather_data.keys():
            month = int(date.split('-')[1])
            if 3 <= month <= 5:
                seasons['wiosna'].append(comfort_scores[date])
            elif 6 <= month <= 8:
                seasons['lato'].append(comfort_scores[date])
            elif 9 <= month <= 11:
                seasons['jesień'].append(comfort_scores[date])
            else:
                seasons['zima'].append(comfort_scores[date])

        # Oblicz średnie dla sezonów
        season_averages = {}
        for season, scores in seasons.items():
            if scores:
                season_averages[season] = sum(scores) / len(scores)
            else:
                season_averages[season] = 0.0

        # Znajdź najlepszą porę roku
        best_season = max(season_averages.items(), key=lambda x: x[1])[0]
        
        # Przygotuj rekomendacje
        recommendations = []
        if best_season:
            recommendations.append(f"Najlepsza pora roku: {best_season}")
        
        if trail_type == 'górski':
            recommendations.append("Unikaj dni z silnym wiatrem i opadami")
        elif trail_type == 'leśny':
            recommendations.append("Dobry wybór nawet w pochmurne dni")
        
        # Dodaj ogólne zalecenia
        if avg_comfort < 50:
            recommendations.append("Zalecana duża ostrożność przy planowaniu wycieczki")
        elif avg_comfort > 70:
            recommendations.append("Bardzo dobre warunki przez większość czasu")

        return {
            "best_dates": best_dates[:5],  # Top 5 najlepszych dat
            "average_comfort": round(avg_comfort, 2),
            "recommendations": ". ".join(recommendations),
            "season_scores": {k: round(v, 2) for k, v in season_averages.items()}
        }
    
    @staticmethod
    def analyze_best_periods(weather_data: Dict[str, Dict[str, Any]], trail_type: str) -> Dict[str, Any]:
        """
        Analizuje dane pogodowe aby znaleźć najlepsze okresy dla danej trasy.
        
        Args:
            weather_data: Słownik z danymi pogodowymi dla różnych dat
            trail_type: Typ trasy (górski, nizinny, leśny, miejski)
            
        Returns:
            Dict zawierający analizę okresów
        """
        if not weather_data:
            return {
                "average_comfort": 0,
                "best_dates": [],
                "season_scores": {
                    "Wiosna": 0,
                    "Lato": 0,
                    "Jesień": 0,
                    "Zima": 0
                },
                "recommendations": "Brak danych do analizy"
            }
            
        # Przygotuj strukturę na wyniki
        comfort_scores = {}
        season_scores = {
            "Wiosna": [],  # Marzec-Maj
            "Lato": [],    # Czerwiec-Sierpień
            "Jesień": [],  # Wrzesień-Listopad
            "Zima": []     # Grudzień-Luty
        }
        
        # Analizuj każdy dzień
        for date_str, data in weather_data.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                month = date.month
                
                # Oblicz indeks komfortu dla danego dnia
                comfort = WeatherUtils.calculate_hiking_comfort(data)
                comfort_scores[date_str] = comfort
                
                # Przypisz wynik do odpowiedniej pory roku
                if 3 <= month <= 5:
                    season_scores["Wiosna"].append(comfort)
                elif 6 <= month <= 8:
                    season_scores["Lato"].append(comfort)
                elif 9 <= month <= 11:
                    season_scores["Jesień"].append(comfort)
                else:
                    season_scores["Zima"].append(comfort)
                    
            except (ValueError, KeyError):
                continue
                
        # Znajdź najlepsze daty (z komfortem > 80)
        best_dates = sorted([
            (date, score) for date, score in comfort_scores.items()
            if score > 80
        ], key=lambda x: x[1], reverse=True)[:5]
        
        # Oblicz średnie dla sezonów
        avg_scores = {}
        for season, scores in season_scores.items():
            avg_scores[season] = round(sum(scores) / len(scores)) if scores else 0
            
        # Określ najlepszą porę roku
        best_season = max(avg_scores.items(), key=lambda x: x[1])[0]
        
        # Przygotuj rekomendacje
        recommendations = []
        if trail_type == "górski":
            if best_season in ["Wiosna", "Jesień"]:
                recommendations.append("Idealne warunki dla tego typu trasy")
            elif best_season == "Lato":
                recommendations.append("Możliwe upały, zalecana wczesna pora dnia")
            else:
                recommendations.append("W zimie wymagane dodatkowe przygotowanie")
        elif trail_type in ["leśny", "nizinny"]:
            if best_season in ["Wiosna", "Lato"]:
                recommendations.append("Świetne warunki do wędrówek")
            else:
                recommendations.append("Sprawdź prognozę opadów przed wycieczką")
        
        return {
            "average_comfort": round(sum(comfort_scores.values()) / len(comfort_scores)) if comfort_scores else 0,
            "best_dates": [date for date, _ in best_dates],
            "season_scores": avg_scores,
            "recommendations": " | ".join(recommendations) if recommendations else "Brak szczególnych zaleceń"
        }