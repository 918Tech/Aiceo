"""
AdTV - Retro Learning & Earning TV Channel dApp
A project managed by the AI CEO system

Features:
- MTV-style retro interface with static effects when changing channels
- Ad integration on all channels
- Learn & earn functionality with questions about ads
- Reward system based on answer streaks
- Bluetooth device detection for group interactions
"""

import os
import random
import json
import time
from datetime import datetime

class AdTVChannel:
    """Represents a TV channel with specific content theme and related ads"""
    
    def __init__(self, channel_id, name, description, category, difficulty="medium"):
        self.channel_id = channel_id
        self.name = name
        self.description = description
        self.category = category
        self.difficulty = difficulty
        self.ads = []
        self.content_blocks = []
        self.questions = []
    
    def add_ad(self, ad):
        """Add an advertisement to this channel"""
        self.ads.append(ad)
        return len(self.ads)
    
    def add_content_block(self, title, content, duration):
        """Add a content segment to this channel"""
        self.content_blocks.append({
            "title": title,
            "content": content,
            "duration": duration
        })
        return len(self.content_blocks)
    
    def add_question(self, question_text, options, correct_answer, points=10):
        """Add a question related to ads shown on this channel"""
        self.questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "points": points
        })
        return len(self.questions)
    
    def get_random_ad(self):
        """Return a random advertisement for this channel"""
        if not self.ads:
            return None
        return random.choice(self.ads)
    
    def get_random_content(self):
        """Return a random content block from this channel"""
        if not self.content_blocks:
            return None
        return random.choice(self.content_blocks)
    
    def get_random_question(self):
        """Return a random question about ads on this channel"""
        if not self.questions:
            return None
        return random.choice(self.questions)
    
    def to_dict(self):
        """Convert channel to dictionary for serialization"""
        return {
            "channel_id": self.channel_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "difficulty": self.difficulty,
            "ads": self.ads,
            "content_blocks": self.content_blocks,
            "questions": self.questions
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create channel from dictionary"""
        channel = cls(
            data["channel_id"],
            data["name"],
            data["description"],
            data["category"],
            data.get("difficulty", "medium")
        )
        channel.ads = data.get("ads", [])
        channel.content_blocks = data.get("content_blocks", [])
        channel.questions = data.get("questions", [])
        return channel


class Advertisement:
    """Represents an advertisement with related questions"""
    
    def __init__(self, ad_id, brand, slogan, content, duration=30):
        self.ad_id = ad_id
        self.brand = brand
        self.slogan = slogan
        self.content = content
        self.duration = duration  # in seconds
        self.questions = []
    
    def add_question(self, question_text, options, correct_answer, points=10):
        """Add a question related to this ad"""
        self.questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "points": points
        })
        return len(self.questions)
    
    def to_dict(self):
        """Convert ad to dictionary for serialization"""
        return {
            "ad_id": self.ad_id,
            "brand": self.brand,
            "slogan": self.slogan,
            "content": self.content,
            "duration": self.duration,
            "questions": self.questions
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create ad from dictionary"""
        ad = cls(
            data["ad_id"],
            data["brand"],
            data["slogan"],
            data["content"],
            data.get("duration", 30)
        )
        ad.questions = data.get("questions", [])
        return ad


class UserProfile:
    """Represents a user profile with points, rewards and history"""
    
    def __init__(self, user_id, username, email=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.points = 0
        self.streak = 0
        self.max_streak = 0
        self.rewards = []
        self.watch_history = []
        self.answer_history = []
        self.device_id = None
        self.created_at = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()
    
    def add_points(self, points, reason="correct answer"):
        """Add points to user profile"""
        self.points += points
        self.last_active = datetime.now().isoformat()
        return self.points
    
    def increase_streak(self):
        """Increase user's correct answer streak"""
        self.streak += 1
        if self.streak > self.max_streak:
            self.max_streak = self.streak
        self.last_active = datetime.now().isoformat()
        return self.streak
    
    def reset_streak(self):
        """Reset user's correct answer streak"""
        self.streak = 0
        self.last_active = datetime.now().isoformat()
        return self.streak
    
    def add_to_watch_history(self, channel_id, duration):
        """Add channel watch to history"""
        self.watch_history.append({
            "channel_id": channel_id,
            "timestamp": datetime.now().isoformat(),
            "duration": duration
        })
        self.last_active = datetime.now().isoformat()
    
    def add_to_answer_history(self, question, answer, correct, points):
        """Add question answer to history"""
        self.answer_history.append({
            "question": question,
            "answer": answer,
            "correct": correct,
            "points": points,
            "timestamp": datetime.now().isoformat()
        })
        self.last_active = datetime.now().isoformat()
    
    def add_reward(self, reward_id, reward_name, points_cost):
        """Add a reward to user profile"""
        if self.points >= points_cost:
            self.points -= points_cost
            self.rewards.append({
                "reward_id": reward_id,
                "reward_name": reward_name,
                "redeemed_at": datetime.now().isoformat(),
                "points_cost": points_cost
            })
            self.last_active = datetime.now().isoformat()
            return True
        return False
    
    def register_device(self, device_id):
        """Register a Bluetooth device with user profile"""
        self.device_id = device_id
        self.last_active = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert user profile to dictionary for serialization"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "points": self.points,
            "streak": self.streak,
            "max_streak": self.max_streak,
            "rewards": self.rewards,
            "watch_history": self.watch_history,
            "answer_history": self.answer_history,
            "device_id": self.device_id,
            "created_at": self.created_at,
            "last_active": self.last_active
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user profile from dictionary"""
        user = cls(
            data["user_id"],
            data["username"],
            data.get("email")
        )
        user.points = data.get("points", 0)
        user.streak = data.get("streak", 0)
        user.max_streak = data.get("max_streak", 0)
        user.rewards = data.get("rewards", [])
        user.watch_history = data.get("watch_history", [])
        user.answer_history = data.get("answer_history", [])
        user.device_id = data.get("device_id")
        user.created_at = data.get("created_at", user.created_at)
        user.last_active = data.get("last_active", user.last_active)
        return user


class AdTVSystem:
    """Main system for managing AdTV channels, ads, users and rewards"""
    
    def __init__(self, data_dir="adtv_data"):
        self.data_dir = data_dir
        self.channels = {}
        self.ads = {}
        self.users = {}
        self.rewards = {}
        self.slogan_detection = {}
        self.bluetooth_devices = set()
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Load any existing data
        self._load_data()
    
    def _load_data(self):
        """Load data from files"""
        try:
            # Load channels
            channels_file = os.path.join(self.data_dir, "channels.json")
            if os.path.exists(channels_file):
                with open(channels_file, 'r') as f:
                    channels_data = json.load(f)
                    for channel_data in channels_data:
                        channel = AdTVChannel.from_dict(channel_data)
                        self.channels[channel.channel_id] = channel
            
            # Load ads
            ads_file = os.path.join(self.data_dir, "ads.json")
            if os.path.exists(ads_file):
                with open(ads_file, 'r') as f:
                    ads_data = json.load(f)
                    for ad_data in ads_data:
                        ad = Advertisement.from_dict(ad_data)
                        self.ads[ad.ad_id] = ad
            
            # Load users
            users_file = os.path.join(self.data_dir, "users.json")
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users_data = json.load(f)
                    for user_data in users_data:
                        user = UserProfile.from_dict(user_data)
                        self.users[user.user_id] = user
            
            # Load rewards
            rewards_file = os.path.join(self.data_dir, "rewards.json")
            if os.path.exists(rewards_file):
                with open(rewards_file, 'r') as f:
                    self.rewards = json.load(f)
                    
            # Load slogan detection data
            slogan_file = os.path.join(self.data_dir, "slogans.json")
            if os.path.exists(slogan_file):
                with open(slogan_file, 'r') as f:
                    self.slogan_detection = json.load(f)
                    
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def _save_data(self):
        """Save data to files"""
        try:
            # Save channels
            channels_data = [channel.to_dict() for channel in self.channels.values()]
            with open(os.path.join(self.data_dir, "channels.json"), 'w') as f:
                json.dump(channels_data, f, indent=4)
            
            # Save ads
            ads_data = [ad.to_dict() for ad in self.ads.values()]
            with open(os.path.join(self.data_dir, "ads.json"), 'w') as f:
                json.dump(ads_data, f, indent=4)
            
            # Save users
            users_data = [user.to_dict() for user in self.users.values()]
            with open(os.path.join(self.data_dir, "users.json"), 'w') as f:
                json.dump(users_data, f, indent=4)
            
            # Save rewards
            with open(os.path.join(self.data_dir, "rewards.json"), 'w') as f:
                json.dump(self.rewards, f, indent=4)
                
            # Save slogan detection data
            with open(os.path.join(self.data_dir, "slogans.json"), 'w') as f:
                json.dump(self.slogan_detection, f, indent=4)
                
        except Exception as e:
            print(f"Error saving data: {str(e)}")
    
    def create_channel(self, name, description, category, difficulty="medium"):
        """Create a new channel"""
        channel_id = f"ch_{int(time.time())}_{len(self.channels) + 1}"
        channel = AdTVChannel(channel_id, name, description, category, difficulty)
        self.channels[channel_id] = channel
        self._save_data()
        return channel
    
    def create_ad(self, brand, slogan, content, duration=30):
        """Create a new advertisement"""
        ad_id = f"ad_{int(time.time())}_{len(self.ads) + 1}"
        ad = Advertisement(ad_id, brand, slogan, content, duration)
        self.ads[ad_id] = ad
        
        # Register slogan for detection
        self.slogan_detection[slogan] = {
            "brand": brand,
            "ad_id": ad_id,
            "points": 5
        }
        
        self._save_data()
        return ad
    
    def add_ad_to_channel(self, channel_id, ad_id):
        """Add an advertisement to a specific channel"""
        if channel_id not in self.channels or ad_id not in self.ads:
            return False
            
        self.channels[channel_id].add_ad(self.ads[ad_id].to_dict())
        self._save_data()
        return True
    
    def create_user(self, username, email=None):
        """Create a new user profile"""
        user_id = f"user_{int(time.time())}_{len(self.users) + 1}"
        user = UserProfile(user_id, username, email)
        self.users[user_id] = user
        self._save_data()
        return user
    
    def add_reward(self, reward_id, reward_name, description, points_cost, inventory=None):
        """Add a reward that users can redeem with points"""
        self.rewards[reward_id] = {
            "name": reward_name,
            "description": description,
            "points_cost": points_cost,
            "inventory": inventory,
            "created_at": datetime.now().isoformat()
        }
        self._save_data()
        return self.rewards[reward_id]
    
    def redeem_reward(self, user_id, reward_id):
        """Allow a user to redeem a reward with their points"""
        if user_id not in self.users or reward_id not in self.rewards:
            return False
            
        user = self.users[user_id]
        reward = self.rewards[reward_id]
        
        # Check if inventory is available
        if reward.get("inventory") is not None and reward["inventory"] <= 0:
            return False
        
        # Attempt to redeem the reward
        if user.add_reward(reward_id, reward["name"], reward["points_cost"]):
            # Decrement inventory if applicable
            if reward.get("inventory") is not None:
                reward["inventory"] -= 1
            
            self._save_data()
            return True
        
        return False
    
    def record_watch(self, user_id, channel_id, duration):
        """Record that a user watched a channel for a duration"""
        if user_id not in self.users or channel_id not in self.channels:
            return False
            
        self.users[user_id].add_to_watch_history(channel_id, duration)
        self._save_data()
        return True
    
    def answer_question(self, user_id, question, answer):
        """Process a user's answer to a question"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        correct = (answer == question["correct_answer"])
        points = question["points"] if correct else 0
        
        # Apply streak multiplier if answer is correct
        if correct:
            user.increase_streak()
            # Apply streak multiplier (max 3x)
            streak_multiplier = min(3, 1 + (user.streak // 5) * 0.5)
            points = int(points * streak_multiplier)
            user.add_points(points, "correct answer with streak")
        else:
            user.reset_streak()
        
        # Record the answer in history
        user.add_to_answer_history(question["question"], answer, correct, points)
        self._save_data()
        
        return {
            "correct": correct,
            "points": points,
            "streak": user.streak,
            "total_points": user.points
        }
    
    def detect_bluetooth_device(self, device_id):
        """Detect a Bluetooth device nearby"""
        self.bluetooth_devices.add(device_id)
        return True
    
    def register_device_to_user(self, user_id, device_id):
        """Register a Bluetooth device to a user"""
        if user_id not in self.users:
            return False
            
        self.users[user_id].register_device(device_id)
        self._save_data()
        return True
    
    def detect_slogan(self, user_id, slogan):
        """Detect when a user says a brand slogan"""
        if user_id not in self.users or slogan not in self.slogan_detection:
            return False
            
        user = self.users[user_id]
        slogan_data = self.slogan_detection[slogan]
        points = slogan_data["points"]
        
        # Award points for saying the slogan
        user.add_points(points, f"said slogan: {slogan}")
        self._save_data()
        
        return {
            "brand": slogan_data["brand"],
            "slogan": slogan,
            "points": points,
            "total_points": user.points
        }
    
    def get_nearby_users(self, user_id):
        """Get users who are nearby based on Bluetooth detection"""
        if user_id not in self.users:
            return []
            
        current_device = self.users[user_id].device_id
        if not current_device or current_device not in self.bluetooth_devices:
            return []
            
        # Find users with devices that are in our Bluetooth detection list
        nearby_users = []
        for other_id, other_user in self.users.items():
            if other_id != user_id and other_user.device_id in self.bluetooth_devices:
                nearby_users.append({
                    "user_id": other_id,
                    "username": other_user.username
                })
                
        return nearby_users
    
    def generate_ad_block(self, channel_id, block_size=5):
        """Generate a block of ads for a channel"""
        if channel_id not in self.channels:
            return []
            
        channel = self.channels[channel_id]
        ads_block = []
        
        # Generate a block of ads (either from channel-specific ads or general pool)
        for _ in range(block_size):
            if channel.ads and random.random() < 0.7:  # 70% chance of channel-specific ad
                ads_block.append(random.choice(channel.ads))
            elif self.ads:  # Otherwise pick from general ad pool
                ads_block.append(random.choice(list(self.ads.values())).to_dict())
        
        return ads_block
    
    def generate_quiz_for_ads(self, ads_block):
        """Generate quiz questions for a block of ads"""
        quiz = []
        
        for ad_data in ads_block:
            ad_id = ad_data.get("ad_id")
            if ad_id in self.ads and self.ads[ad_id].questions:
                # Use questions specifically created for this ad
                question = random.choice(self.ads[ad_id].questions)
                quiz.append(question)
            else:
                # Generate a basic question about the ad
                brand = ad_data.get("brand", "Unknown")
                slogan = ad_data.get("slogan", "")
                
                # Create a simple question about the brand or slogan
                if random.random() < 0.5 and slogan:
                    quiz.append({
                        "question": f"What is the slogan for {brand}?",
                        "options": [
                            slogan,
                            f"The best {brand} in town",
                            f"{brand} - always the first choice",
                            f"Experience the {brand} difference"
                        ],
                        "correct_answer": slogan,
                        "points": 10
                    })
                else:
                    quiz.append({
                        "question": f"Which brand was featured in the ad with '{slogan[:20]}...'?",
                        "options": [
                            brand,
                            f"Super{brand}",
                            f"My{brand}",
                            f"{brand} Plus"
                        ],
                        "correct_answer": brand,
                        "points": 10
                    })
        
        return quiz
    
    def get_user_stats(self, user_id):
        """Get comprehensive stats for a user"""
        if user_id not in self.users:
            return None
            
        user = self.users[user_id]
        
        # Calculate watch time
        total_watch_time = sum(entry["duration"] for entry in user.watch_history)
        
        # Calculate correct answer rate
        if user.answer_history:
            correct_answers = sum(1 for entry in user.answer_history if entry["correct"])
            answer_rate = correct_answers / len(user.answer_history)
        else:
            answer_rate = 0
        
        # Get most watched channel
        channel_watches = {}
        for watch in user.watch_history:
            channel_id = watch["channel_id"]
            if channel_id in channel_watches:
                channel_watches[channel_id] += watch["duration"]
            else:
                channel_watches[channel_id] = watch["duration"]
                
        most_watched = None
        most_watched_time = 0
        for channel_id, watch_time in channel_watches.items():
            if watch_time > most_watched_time and channel_id in self.channels:
                most_watched = self.channels[channel_id].name
                most_watched_time = watch_time
        
        return {
            "username": user.username,
            "points": user.points,
            "current_streak": user.streak,
            "max_streak": user.max_streak,
            "total_watch_time": total_watch_time,
            "questions_answered": len(user.answer_history),
            "correct_answer_rate": answer_rate,
            "rewards_redeemed": len(user.rewards),
            "most_watched_channel": most_watched,
            "last_active": user.last_active
        }


# Example usage code for setting up a basic AdTV system
def create_sample_adtv():
    """Create a sample AdTV system with channels, ads, and questions"""
    adtv = AdTVSystem()
    
    # Create some channels based on the specified categories
    channels = [
        adtv.create_channel("TV & Movie Trivia", "Earn prizes by answering trivia about TV shows and movies", "Entertainment"),
        adtv.create_channel("Tech Trade", "Learn technical trade skills and earn certifications", "Education"),
        adtv.create_channel("Code Academy", "Learn coding and get real job opportunities", "Education"),
        adtv.create_channel("AI & Automation", "Master AI and automation skills for the future", "Technology"),
        adtv.create_channel("Finance Hub", "Learn investing and personal finance strategies", "Finance"),
        adtv.create_channel("Legal Corner", "Understand laws and legal rights that affect you", "Education"),
        adtv.create_channel("Entrepreneur TV", "Learn about business and side hustle opportunities", "Business"),
        adtv.create_channel("Language Master", "Learn new languages effectively", "Education"),
        adtv.create_channel("Fitness & Health", "Improve your health and fitness", "Lifestyle"),
        adtv.create_channel("History Channel", "Explore history and interesting conspiracy theories", "Entertainment"),
        adtv.create_channel("Cybersecurity", "Learn ethical hacking and cybersecurity skills", "Technology"),
        adtv.create_channel("Space Explorer", "Journey through space and learn about science", "Science"),
        adtv.create_channel("Music Studio", "Learn music production and DJ skills", "Entertainment"),
        adtv.create_channel("Military Tactics", "Understand military strategy and tactics", "Education")
    ]
    
    # Create some sample ads
    ads = [
        adtv.create_ad("TechBoost", "Level up your future", "Ad showing young professionals advancing in tech careers", 45),
        adtv.create_ad("CodeMasters", "Code your dreams into reality", "Animated ad showing code turning into real-world applications", 30),
        adtv.create_ad("FinanceGenius", "Smart money for smart people", "Ad showing people making wise investment decisions", 60),
        adtv.create_ad("HealthPlus", "Your health, our priority", "People enjoying active lifestyles and healthy eating", 30),
        adtv.create_ad("SpaceTech", "Reach for the stars", "Futuristic ad about space technology and exploration", 45)
    ]
    
    # Add questions to ads
    ads[0].add_question(
        "What is TechBoost's slogan?",
        ["Tech your way forward", "Level up your future", "Boost your tech skills", "Tomorrow's tech today"],
        "Level up your future",
        15
    )
    
    ads[1].add_question(
        "What does the CodeMasters ad show transforming into real applications?",
        ["Robots", "Code", "Engineers", "Computers"],
        "Code",
        10
    )
    
    ads[2].add_question(
        "According to the ad, FinanceGenius is for whom?",
        ["Rich people", "Bankers", "Smart people", "College students"],
        "Smart people",
        10
    )
    
    # Add ads to channels
    for channel in channels:
        # Add 2-3 random ads to each channel
        for _ in range(random.randint(2, 3)):
            ad = random.choice(ads)
            adtv.add_ad_to_channel(channel.channel_id, ad.ad_id)
    
    # Create some sample content for each channel
    for channel in channels:
        # Add 3-5 content blocks per channel
        for i in range(random.randint(3, 5)):
            channel.add_content_block(
                f"Content Block {i+1}",
                f"Sample content for {channel.name} - Block {i+1}",
                random.randint(5, 15) * 60  # 5-15 minutes
            )
    
    # Create some sample rewards
    adtv.add_reward("reward_1", "Gift Card $10", "Digital gift card for popular online stores", 1000, 50)
    adtv.add_reward("reward_2", "Premium Membership", "1 month of ad-free viewing", 750, 100)
    adtv.add_reward("reward_3", "Exclusive Content", "Access to exclusive premium content", 500, None)
    adtv.add_reward("reward_4", "Virtual Swag", "Digital merchandise and profile items", 250, None)
    
    # Create a sample user
    user = adtv.create_user("TestUser", "test@example.com")
    
    # Save all data
    adtv._save_data()
    
    return adtv


if __name__ == "__main__":
    # Create a sample AdTV system
    print("Creating sample AdTV system...")
    adtv = create_sample_adtv()
    print(f"Created AdTV system with {len(adtv.channels)} channels and {len(adtv.ads)} ads")
    print("Data saved to the adtv_data directory")