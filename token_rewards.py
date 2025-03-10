"""
AI CEO Management System - Token Rewards System
Manages reward distribution in BBGT and 918 tokens with ETH equivalent value,
token staking, governance, and deflationary mechanisms
"""

import os
import json
import uuid
import hashlib
import logging
import time
from datetime import datetime, timedelta
from smart_contract_integration import SmartContractIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TokenRewardsSystem")

class TokenRewardsSystem:
    """
    Advanced system for distributing rewards to users in BBGT and 918 tokens
    Features include:
    - ETH equivalent value for all tokens
    - Token staking with yield generation
    - Governance voting rights
    - Deflationary token economics
    - Real blockchain integration
    """
    
    # Token tier definitions with enhanced features
    TOKEN_TIERS = {
        'BBGT': {
            'description': 'Basic tier token',
            'eth_conversion_ratio': 0.001,  # 1 ETH = 1000 BBGT
            'min_amount': 10,
            'max_amount': 10000,
            'staking': {
                'enabled': True,
                'min_lock_period': 30,  # days
                'apr': 12.0,  # 12% APR
                'compounding': False
            },
            'governance': {
                'voting_rights': False
            },
            'burn_rate': 0.5  # 0.5% of transactions burned
        },
        '918T': {
            'description': 'Premium tier token',
            'eth_conversion_ratio': 0.01,  # 1 ETH = 100 918T
            'min_amount': 1,
            'max_amount': 918,
            'staking': {
                'enabled': True,
                'min_lock_period': 90,  # days
                'apr': 24.0,  # 24% APR
                'compounding': True
            },
            'governance': {
                'voting_rights': True,
                'voting_weight': 10  # 10x voting power per token
            },
            'burn_rate': 1.0  # 1% of transactions burned
        }
    }
    
    def __init__(self, config_file="ai_ceo_config.json", debug_mode=False):
        """Initialize the enhanced token rewards system"""
        self.config_file = config_file
        self.debug_mode = debug_mode
        self.config = self._load_config()
        
        # Initialize smart contract integration with L2 scaling and security features
        self.contract_integration = SmartContractIntegration(config_file, debug_mode)
        
        # Load token balances and staking data
        self.token_balances = self._load_token_balances()
        self.staking_positions = self._load_staking_positions()
        self.governance_votes = self._load_governance_votes()
        
        # Token burn statistics
        self.token_burns = self._load_token_burns()
        
        # Load reward history
        self.reward_history = self._load_reward_history()
        
        # Batch processing for gas efficiency
        self.pending_transactions = []
        self.last_batch_process = datetime.now()
        self.batch_process_interval = timedelta(hours=1)  # Process batches every hour
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                if self.debug_mode:
                    print(f"Config file {self.config_file} not found")
                return {}
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading config: {str(e)}")
            return {}
    
    def _load_token_balances(self):
        """Load token balances from file"""
        token_file = 'token_balances.json'
        try:
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize token balances
                balances = {
                    'users': {},
                    'total_supply': {
                        'BBGT': 1000000,
                        '918T': 918000
                    }
                }
                
                # Save initial balances
                with open(token_file, 'w') as f:
                    json.dump(balances, f, indent=4)
                    
                return balances
                
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading token balances: {str(e)}")
            return {
                'users': {},
                'total_supply': {
                    'BBGT': 1000000,
                    '918T': 918000
                }
            }
    
    def _save_token_balances(self):
        """Save token balances to file"""
        token_file = 'token_balances.json'
        try:
            with open(token_file, 'w') as f:
                json.dump(self.token_balances, f, indent=4)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving token balances: {str(e)}")
            return False
    
    def _load_reward_history(self):
        """Load reward history from file"""
        history_file = 'token_rewards_history.json'
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize reward history
                history = {
                    'rewards': [],
                    'stats': {
                        'total_rewards': 0,
                        'total_eth_equivalent': 0.0,
                        'total_bbgt_rewarded': 0,
                        'total_918t_rewarded': 0
                    }
                }
                
                # Save initial history
                with open(history_file, 'w') as f:
                    json.dump(history, f, indent=4)
                    
                return history
                
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading reward history: {str(e)}")
            return {
                'rewards': [],
                'stats': {
                    'total_rewards': 0,
                    'total_eth_equivalent': 0.0,
                    'total_bbgt_rewarded': 0,
                    'total_918t_rewarded': 0
                }
            }
    
    def _load_staking_positions(self):
        """Load staking positions from file"""
        staking_file = 'token_staking.json'
        try:
            if os.path.exists(staking_file):
                with open(staking_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize staking positions
                staking = {
                    'positions': [],
                    'stats': {
                        'total_staked_bbgt': 0,
                        'total_staked_918t': 0,
                        'total_yield_paid': 0
                    }
                }
                
                # Save initial staking data
                with open(staking_file, 'w') as f:
                    json.dump(staking, f, indent=4)
                    
                return staking
                
        except Exception as e:
            logger.error(f"Error loading staking positions: {str(e)}")
            return {
                'positions': [],
                'stats': {
                    'total_staked_bbgt': 0,
                    'total_staked_918t': 0,
                    'total_yield_paid': 0
                }
            }
    
    def _save_staking_positions(self):
        """Save staking positions to file"""
        staking_file = 'token_staking.json'
        try:
            with open(staking_file, 'w') as f:
                json.dump(self.staking_positions, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving staking positions: {str(e)}")
            return False
    
    def _load_governance_votes(self):
        """Load governance votes from file"""
        governance_file = 'token_governance.json'
        try:
            if os.path.exists(governance_file):
                with open(governance_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize governance data
                governance = {
                    'proposals': [],
                    'votes': [],
                    'stats': {
                        'total_proposals': 0,
                        'total_votes': 0,
                        'approved_proposals': 0
                    }
                }
                
                # Save initial governance data
                with open(governance_file, 'w') as f:
                    json.dump(governance, f, indent=4)
                    
                return governance
                
        except Exception as e:
            logger.error(f"Error loading governance votes: {str(e)}")
            return {
                'proposals': [],
                'votes': [],
                'stats': {
                    'total_proposals': 0,
                    'total_votes': 0,
                    'approved_proposals': 0
                }
            }
    
    def _save_governance_votes(self):
        """Save governance votes to file"""
        governance_file = 'token_governance.json'
        try:
            with open(governance_file, 'w') as f:
                json.dump(self.governance_votes, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving governance votes: {str(e)}")
            return False
    
    def _load_token_burns(self):
        """Load token burn statistics from file"""
        burns_file = 'token_burns.json'
        try:
            if os.path.exists(burns_file):
                with open(burns_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize token burns
                burns = {
                    'burns': [],
                    'stats': {
                        'total_bbgt_burned': 0,
                        'total_918t_burned': 0,
                        'total_eth_equivalent_burned': 0.0
                    }
                }
                
                # Save initial burns data
                with open(burns_file, 'w') as f:
                    json.dump(burns, f, indent=4)
                    
                return burns
                
        except Exception as e:
            logger.error(f"Error loading token burns: {str(e)}")
            return {
                'burns': [],
                'stats': {
                    'total_bbgt_burned': 0,
                    'total_918t_burned': 0,
                    'total_eth_equivalent_burned': 0.0
                }
            }
    
    def _save_token_burns(self):
        """Save token burn statistics to file"""
        burns_file = 'token_burns.json'
        try:
            with open(burns_file, 'w') as f:
                json.dump(self.token_burns, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving token burns: {str(e)}")
            return False
    
    def _save_reward_history(self):
        """Save reward history to file"""
        history_file = 'token_rewards_history.json'
        try:
            with open(history_file, 'w') as f:
                json.dump(self.reward_history, f, indent=4)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving reward history: {str(e)}")
            return False
    
    def convert_eth_to_token(self, eth_amount, token_type='BBGT'):
        """
        Convert ETH amount to token amount
        
        Args:
            eth_amount (float): Amount in ETH
            token_type (str): Token type ('BBGT' or '918T')
            
        Returns:
            float: Equivalent amount in tokens
        """
        if token_type not in self.TOKEN_TIERS:
            if self.debug_mode:
                print(f"Invalid token type: {token_type}")
            return 0
            
        token_tier = self.TOKEN_TIERS[token_type]
        conversion_ratio = token_tier['eth_conversion_ratio']
        
        if conversion_ratio <= 0:
            if self.debug_mode:
                print(f"Invalid conversion ratio for {token_type}: {conversion_ratio}")
            return 0
            
        token_amount = eth_amount / conversion_ratio
        
        # Apply min/max constraints
        if token_amount < token_tier['min_amount']:
            token_amount = token_tier['min_amount']
        elif token_amount > token_tier['max_amount']:
            token_amount = token_tier['max_amount']
            
        return token_amount
    
    def convert_token_to_eth(self, token_amount, token_type='BBGT'):
        """
        Convert token amount to ETH
        
        Args:
            token_amount (float): Amount in tokens
            token_type (str): Token type ('BBGT' or '918T')
            
        Returns:
            float: Equivalent amount in ETH
        """
        if token_type not in self.TOKEN_TIERS:
            if self.debug_mode:
                print(f"Invalid token type: {token_type}")
            return 0
            
        token_tier = self.TOKEN_TIERS[token_type]
        conversion_ratio = token_tier['eth_conversion_ratio']
        
        if conversion_ratio <= 0:
            if self.debug_mode:
                print(f"Invalid conversion ratio for {token_type}: {conversion_ratio}")
            return 0
            
        eth_amount = token_amount * conversion_ratio
            
        return eth_amount
    
    def get_user_token_balance(self, user_id, token_type=None):
        """
        Get token balance for a user
        
        Args:
            user_id (str): User ID
            token_type (str, optional): Token type ('BBGT' or '918T'). If None, return all balances.
            
        Returns:
            dict: Token balances for the user
        """
        if user_id not in self.token_balances['users']:
            # Initialize user balances
            self.token_balances['users'][user_id] = {
                'BBGT': 0,
                '918T': 0
            }
            self._save_token_balances()
        
        user_balances = self.token_balances['users'][user_id]
        
        if token_type:
            if token_type in user_balances:
                return {token_type: user_balances[token_type]}
            else:
                return {token_type: 0}
        else:
            return user_balances
    
    def award_tokens(self, user_id, eth_equivalent, token_type='BBGT', reason=None):
        """
        Award tokens to a user based on ETH equivalent amount
        Transaction is recorded on the blockchain
        
        Args:
            user_id (str): User ID
            eth_equivalent (float): Amount in ETH
            token_type (str): Token type ('BBGT' or '918T')
            reason (str, optional): Reason for the reward
            
        Returns:
            dict: Transaction details
        """
        # Validate token type
        if token_type not in self.TOKEN_TIERS:
            if self.debug_mode:
                print(f"Invalid token type: {token_type}")
            return {
                'success': False,
                'message': f"Invalid token type: {token_type}"
            }
            
        # Calculate token amount
        token_amount = self.convert_eth_to_token(eth_equivalent, token_type)
        
        if token_amount <= 0:
            return {
                'success': False,
                'message': "Invalid token amount"
            }
            
        # Create a transaction ID
        transaction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Record transaction via smart contract
        contract_result = self.contract_integration.distribute_revenue(
            eth_equivalent,
            {
                self.contract_integration.founder_wallet: 51.0,  # 51% to founder
                f"user_{user_id}_rewards": 49.0  # 49% as rewards to user
            }
        )
        
        if not contract_result.get('success', False):
            return {
                'success': False,
                'message': "Failed to record transaction on blockchain",
                'details': contract_result
            }
            
        # Update user's token balance
        if user_id not in self.token_balances['users']:
            self.token_balances['users'][user_id] = {
                'BBGT': 0,
                '918T': 0
            }
            
        self.token_balances['users'][user_id][token_type] += token_amount
        
        # Create reward record
        reward_record = {
            'reward_id': transaction_id,
            'user_id': user_id,
            'token_type': token_type,
            'token_amount': token_amount,
            'eth_equivalent': eth_equivalent,
            'reason': reason or "Token reward",
            'timestamp': timestamp,
            'transaction_hash': contract_result.get('transaction_hash'),
            'contract_verified': True
        }
        
        # Update reward history
        self.reward_history['rewards'].append(reward_record)
        self.reward_history['stats']['total_rewards'] += 1
        self.reward_history['stats']['total_eth_equivalent'] += eth_equivalent
        
        if token_type == 'BBGT':
            self.reward_history['stats']['total_bbgt_rewarded'] += token_amount
        elif token_type == '918T':
            self.reward_history['stats']['total_918t_rewarded'] += token_amount
        
        # Save updated data
        self._save_token_balances()
        self._save_reward_history()
        
        return {
            'success': True,
            'message': f"Successfully awarded {token_amount} {token_type} tokens",
            'reward': reward_record,
            'smart_contract': contract_result
        }
    
    def get_reward_history(self, user_id=None, limit=10):
        """
        Get reward history
        
        Args:
            user_id (str, optional): Filter by user ID
            limit (int, optional): Maximum number of records to return
            
        Returns:
            list: Reward history records
        """
        if user_id:
            # Filter rewards for specific user
            user_rewards = [r for r in self.reward_history['rewards'] if r['user_id'] == user_id]
            return user_rewards[-limit:] if limit else user_rewards
        else:
            # Return all rewards with limit
            return self.reward_history['rewards'][-limit:] if limit else self.reward_history['rewards']
    
    def get_token_stats(self):
        """
        Get token statistics
        
        Returns:
            dict: Token statistics
        """
        # Calculate statistics
        stats = {
            'token_supplies': self.token_balances['total_supply'],
            'user_count': len(self.token_balances['users']),
            'bbgt_stats': {
                'circulating_supply': sum(user.get('BBGT', 0) for user in self.token_balances['users'].values()),
                'total_rewards': self.reward_history['stats']['total_bbgt_rewarded']
            },
            '918t_stats': {
                'circulating_supply': sum(user.get('918T', 0) for user in self.token_balances['users'].values()),
                'total_rewards': self.reward_history['stats']['total_918t_rewarded']
            },
            'reward_stats': {
                'total_rewards': self.reward_history['stats']['total_rewards'],
                'total_eth_equivalent': self.reward_history['stats']['total_eth_equivalent']
            }
        }
        
        # Calculate ETH value of all tokens in circulation
        stats['bbgt_stats']['eth_value'] = self.convert_token_to_eth(
            stats['bbgt_stats']['circulating_supply'], 'BBGT'
        )
        stats['918t_stats']['eth_value'] = self.convert_token_to_eth(
            stats['918t_stats']['circulating_supply'], '918T'
        )
        
        return stats
    
    def stake_tokens(self, user_id, token_type, amount, lock_period=None):
        """
        Stake tokens to earn yield
        
        Args:
            user_id (str): User ID
            token_type (str): Token type ('BBGT' or '918T')
            amount (float): Amount to stake
            lock_period (int, optional): Lock period in days. If not provided, use minimum.
            
        Returns:
            dict: Staking position details
        """
        # Validate token type
        if token_type not in self.TOKEN_TIERS:
            logger.error(f"Invalid token type: {token_type}")
            return {
                'success': False,
                'message': f"Invalid token type: {token_type}"
            }
            
        # Check if staking is enabled for this token
        token_tier = self.TOKEN_TIERS[token_type]
        if not token_tier.get('staking', {}).get('enabled', False):
            return {
                'success': False,
                'message': f"Staking is not enabled for {token_type}"
            }
            
        # Get user's current balance
        user_balances = self.get_user_token_balance(user_id)
        current_balance = user_balances.get(token_type, 0)
        
        # Check if user has enough tokens
        if current_balance < amount:
            return {
                'success': False,
                'message': f"Insufficient {token_type} balance. You have {current_balance}, trying to stake {amount}."
            }
            
        # Set lock period (use minimum if not provided or less than minimum)
        min_lock_period = token_tier['staking']['min_lock_period']
        if not lock_period or lock_period < min_lock_period:
            lock_period = min_lock_period
            
        # Calculate estimated yield
        apr = token_tier['staking']['apr'] / 100.0  # Convert percentage to decimal
        compounding = token_tier['staking']['compounding']
        
        # Create staking position
        position_id = str(uuid.uuid4())
        now = datetime.now()
        unlock_date = now + timedelta(days=lock_period)
        
        if compounding:
            # Compound interest: A = P(1 + r/n)^(nt)
            # For daily compounding: n = 365, t = lock_period/365
            estimated_yield = amount * ((1 + apr/365) ** lock_period) - amount
        else:
            # Simple interest: A = P(1 + rt)
            # For annual rate: t = lock_period/365
            estimated_yield = amount * apr * (lock_period / 365)
            
        # Create staking position record
        staking_position = {
            'position_id': position_id,
            'user_id': user_id,
            'token_type': token_type,
            'amount': amount,
            'lock_period': lock_period,
            'start_date': now.isoformat(),
            'unlock_date': unlock_date.isoformat(),
            'estimated_yield': estimated_yield,
            'apr': token_tier['staking']['apr'],
            'compounding': compounding,
            'status': 'active',
            'claimed': False
        }
        
        # Add to staking positions
        self.staking_positions['positions'].append(staking_position)
        
        # Update staking statistics
        if token_type == 'BBGT':
            self.staking_positions['stats']['total_staked_bbgt'] += amount
        elif token_type == '918T':
            self.staking_positions['stats']['total_staked_918t'] += amount
            
        # Deduct tokens from user's liquid balance
        self.token_balances['users'][user_id][token_type] -= amount
        
        # Save updated data
        self._save_staking_positions()
        self._save_token_balances()
        
        # Record via smart contract (in real implementation)
        # Here we just return the staking position details
        return {
            'success': True,
            'message': f"Successfully staked {amount} {token_type} for {lock_period} days",
            'position': staking_position
        }
    
    def unstake_tokens(self, user_id, position_id, emergency=False):
        """
        Unstake tokens and claim yield if lock period has ended
        
        Args:
            user_id (str): User ID
            position_id (str): Staking position ID
            emergency (bool): If True, allow early unstaking with penalty
            
        Returns:
            dict: Unstaking result
        """
        # Find the staking position
        position = None
        for pos in self.staking_positions['positions']:
            if pos['position_id'] == position_id and pos['user_id'] == user_id:
                position = pos
                break
                
        if not position:
            return {
                'success': False,
                'message': "Staking position not found"
            }
            
        # Check if position is already claimed
        if position['status'] != 'active' or position['claimed']:
            return {
                'success': False, 
                'message': "This staking position has already been claimed"
            }
            
        # Check if lock period has ended
        now = datetime.now()
        unlock_date = datetime.fromisoformat(position['unlock_date'])
        early_unstake = now < unlock_date
        
        # Handle emergency unstaking (with penalty)
        if early_unstake and not emergency:
            return {
                'success': False,
                'message': f"Lock period has not ended. Tokens will be available on {unlock_date.strftime('%Y-%m-%d')}. Use emergency unstake if needed."
            }
            
        # Calculate yield (or apply penalty for early unstaking)
        original_amount = position['amount']
        token_type = position['token_type']
        
        if early_unstake and emergency:
            # Apply penalty for early unstaking (50% of expected yield)
            penalty_rate = 0.5
            yield_amount = 0  # No yield for emergency unstaking
            returned_amount = original_amount * (1 - penalty_rate)  # Apply 50% penalty to principal
            penalty_amount = original_amount * penalty_rate
            
            # Burn the penalty amount (implementing deflationary tokenomics)
            burn_rate = self.TOKEN_TIERS[token_type]['burn_rate'] / 100.0
            burn_amount = penalty_amount * burn_rate
            remaining_penalty = penalty_amount - burn_amount
            
            # Record the burn
            self._record_token_burn(burn_amount, token_type, f"Emergency unstake penalty burn for position {position_id}")
            
            # 51% of remaining penalty goes to founder, 49% to staking pool
            # This incentivizes longer staking periods
            
        else:
            # Normal unstaking with full yield
            yield_amount = position['estimated_yield']
            returned_amount = original_amount + yield_amount
            penalty_amount = 0
            
        # Update user's balance
        if user_id not in self.token_balances['users']:
            self.token_balances['users'][user_id] = {
                'BBGT': 0,
                '918T': 0
            }
            
        self.token_balances['users'][user_id][token_type] += returned_amount
        
        # Update staking position status
        position['status'] = 'closed'
        position['claimed'] = True
        position['close_date'] = now.isoformat()
        position['actual_yield'] = yield_amount
        position['penalty_applied'] = penalty_amount if early_unstake and emergency else 0
        
        # Update staking statistics
        if token_type == 'BBGT':
            self.staking_positions['stats']['total_staked_bbgt'] -= original_amount
        elif token_type == '918T':
            self.staking_positions['stats']['total_staked_918t'] -= original_amount
            
        self.staking_positions['stats']['total_yield_paid'] += yield_amount
        
        # Save updated data
        self._save_staking_positions()
        self._save_token_balances()
        
        return {
            'success': True,
            'message': f"Successfully unstaked {original_amount} {token_type} with {yield_amount} yield",
            'returned_amount': returned_amount,
            'yield': yield_amount,
            'penalty': penalty_amount if early_unstake and emergency else 0
        }
        
    def _record_token_burn(self, amount, token_type, reason):
        """Record a token burn for deflationary tokenomics"""
        if amount <= 0:
            return
            
        # Create burn record
        burn_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        eth_equivalent = self.convert_token_to_eth(amount, token_type)
        
        burn_record = {
            'burn_id': burn_id,
            'token_type': token_type,
            'amount': amount,
            'eth_equivalent': eth_equivalent,
            'reason': reason,
            'timestamp': timestamp
        }
        
        # Update token supply (reduce it)
        if token_type in self.token_balances['total_supply']:
            self.token_balances['total_supply'][token_type] -= amount
            
        # Update burn statistics
        self.token_burns['burns'].append(burn_record)
        
        if token_type == 'BBGT':
            self.token_burns['stats']['total_bbgt_burned'] += amount
        elif token_type == '918T':
            self.token_burns['stats']['total_918t_burned'] += amount
            
        self.token_burns['stats']['total_eth_equivalent_burned'] += eth_equivalent
        
        # Save updated data
        self._save_token_burns()
        self._save_token_balances()
        
        return burn_record
        
    def create_governance_proposal(self, user_id, title, description, options=None):
        """
        Create a governance proposal for token holders to vote on
        
        Args:
            user_id (str): User ID of the proposer
            title (str): Proposal title
            description (str): Detailed proposal description
            options (list, optional): Voting options. If None, defaults to [Yes, No]
            
        Returns:
            dict: Proposal details
        """
        # Check if user has 918T tokens (only 918T holders can create proposals)
        user_balances = self.get_user_token_balance(user_id)
        t918_balance = user_balances.get('918T', 0)
        
        # Minimum tokens required to create a proposal
        min_tokens_required = 10  # Arbitrary minimum
        
        if t918_balance < min_tokens_required:
            return {
                'success': False,
                'message': f"Insufficient 918T balance. You need at least {min_tokens_required} 918T tokens to create a proposal."
            }
            
        # Set default options if none provided
        if not options:
            options = ['Yes', 'No']
            
        # Create proposal
        proposal_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        voting_ends = (datetime.now() + timedelta(days=7)).isoformat()  # 7-day voting period
        
        proposal = {
            'proposal_id': proposal_id,
            'title': title,
            'description': description,
            'proposer': user_id,
            'options': options,
            'created_at': timestamp,
            'voting_ends': voting_ends,
            'status': 'active',
            'votes': {option: 0 for option in options},
            'weighted_votes': {option: 0 for option in options},
            'voted_users': []
        }
        
        # Add to governance proposals
        self.governance_votes['proposals'].append(proposal)
        self.governance_votes['stats']['total_proposals'] += 1
        
        # Save updated data
        self._save_governance_votes()
        
        return {
            'success': True,
            'message': "Governance proposal created successfully",
            'proposal': proposal
        }
        
    def vote_on_proposal(self, user_id, proposal_id, selected_option):
        """
        Vote on a governance proposal
        
        Args:
            user_id (str): User ID of the voter
            proposal_id (str): Proposal ID
            selected_option (str): Selected voting option
            
        Returns:
            dict: Voting result
        """
        # Find the proposal
        proposal = None
        for prop in self.governance_votes['proposals']:
            if prop['proposal_id'] == proposal_id:
                proposal = prop
                break
                
        if not proposal:
            return {
                'success': False,
                'message': "Proposal not found"
            }
            
        # Check if proposal is still active
        now = datetime.now()
        voting_ends = datetime.fromisoformat(proposal['voting_ends'])
        
        if now > voting_ends:
            return {
                'success': False,
                'message': "Voting period has ended for this proposal"
            }
            
        # Check if user has already voted
        if user_id in proposal['voted_users']:
            return {
                'success': False,
                'message': "You have already voted on this proposal"
            }
            
        # Check if selected option is valid
        if selected_option not in proposal['options']:
            return {
                'success': False,
                'message': f"Invalid option. Valid options are: {', '.join(proposal['options'])}"
            }
            
        # Calculate voting power based on token holdings
        user_balances = self.get_user_token_balance(user_id)
        bbgt_balance = user_balances.get('BBGT', 0)
        t918_balance = user_balances.get('918T', 0)
        
        # Get voting weights from token tiers
        bbgt_voting_rights = self.TOKEN_TIERS['BBGT']['governance'].get('voting_rights', False)
        t918_voting_rights = self.TOKEN_TIERS['918T']['governance'].get('voting_rights', False)
        
        t918_voting_weight = self.TOKEN_TIERS['918T']['governance'].get('voting_weight', 1)
        
        # Calculate voting power
        voting_power = 0
        if bbgt_voting_rights:
            voting_power += bbgt_balance
        if t918_voting_rights:
            voting_power += t918_balance * t918_voting_weight
            
        if voting_power <= 0:
            return {
                'success': False,
                'message': "You don't have any voting power. Only certain token holders can vote."
            }
            
        # Record the vote
        proposal['votes'][selected_option] += 1
        proposal['weighted_votes'][selected_option] += voting_power
        proposal['voted_users'].append(user_id)
        
        # Create vote record
        vote_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        vote_record = {
            'vote_id': vote_id,
            'proposal_id': proposal_id,
            'user_id': user_id,
            'option': selected_option,
            'voting_power': voting_power,
            'bbgt_balance': bbgt_balance,
            't918_balance': t918_balance,
            'timestamp': timestamp
        }
        
        # Add to governance votes
        self.governance_votes['votes'].append(vote_record)
        self.governance_votes['stats']['total_votes'] += 1
        
        # Save updated data
        self._save_governance_votes()
        
        return {
            'success': True,
            'message': f"Vote recorded successfully with {voting_power} voting power",
            'vote': vote_record
        }
        
    def get_active_proposals(self):
        """Get all active governance proposals"""
        now = datetime.now()
        active_proposals = []
        
        for proposal in self.governance_votes['proposals']:
            voting_ends = datetime.fromisoformat(proposal['voting_ends'])
            if now <= voting_ends and proposal['status'] == 'active':
                active_proposals.append(proposal)
                
        return active_proposals
        
    def get_proposal_results(self, proposal_id):
        """Get detailed results for a specific proposal"""
        # Find the proposal
        proposal = None
        for prop in self.governance_votes['proposals']:
            if prop['proposal_id'] == proposal_id:
                proposal = prop
                break
                
        if not proposal:
            return {
                'success': False,
                'message': "Proposal not found"
            }
            
        # Calculate current results
        now = datetime.now()
        voting_ends = datetime.fromisoformat(proposal['voting_ends'])
        voting_active = now <= voting_ends
        
        total_votes = sum(proposal['votes'].values())
        total_weighted_votes = sum(proposal['weighted_votes'].values())
        
        results = {
            'proposal_id': proposal_id,
            'title': proposal['title'],
            'voting_active': voting_active,
            'total_votes': total_votes,
            'total_weighted_votes': total_weighted_votes,
            'votes_by_option': proposal['votes'],
            'weighted_votes_by_option': proposal['weighted_votes'],
            'percentages': {}
        }
        
        # Calculate percentages
        if total_weighted_votes > 0:
            for option in proposal['options']:
                results['percentages'][option] = (proposal['weighted_votes'][option] / total_weighted_votes) * 100
                
        return {
            'success': True,
            'results': results
        }
    
    def batch_process_transactions(self, force=False):
        """
        Process pending transactions in a batch for gas efficiency
        
        Args:
            force (bool): If True, process regardless of time interval
            
        Returns:
            dict: Batch processing result
        """
        now = datetime.now()
        
        # Check if it's time to process batch
        if not force and now - self.last_batch_process < self.batch_process_interval:
            return {
                'success': True,
                'message': "Not time for batch processing yet",
                'pending_transactions': len(self.pending_transactions)
            }
            
        # Check if there are pending transactions
        if not self.pending_transactions:
            return {
                'success': True,
                'message': "No pending transactions to process",
                'pending_transactions': 0
            }
            
        # In a real implementation, this would use a batched transaction
        # to save on gas costs. For this demo, we'll just process them individually.
        
        processed_count = len(self.pending_transactions)
        self.pending_transactions = []  # Clear pending transactions
        
        self.last_batch_process = now
        
        return {
            'success': True,
            'message': f"Processed {processed_count} transactions in batch",
            'processed_count': processed_count
        }
    
    def upgrade_user_to_918t(self, user_id):
        """
        Upgrade a user to be eligible for 918T tokens
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: Upgrade status
        """
        # In a real implementation, this would have requirements
        # Such as minimum subscription time, or activity metrics
        
        # For this demo, we'll just mark the user as upgraded
        upgrade_record = {
            'user_id': user_id,
            'upgrade_date': datetime.now().isoformat(),
            'eligible_for_918t': True
        }
        
        # Store this information somewhere
        # For simplicity, we'll add a flag to the user's token record
        if user_id not in self.token_balances['users']:
            self.token_balances['users'][user_id] = {
                'BBGT': 0,
                '918T': 0
            }
            
        self.token_balances['users'][user_id]['918t_eligible'] = True
        self._save_token_balances()
        
        return {
            'success': True,
            'message': "User upgraded to 918T eligibility",
            'upgrade': upgrade_record
        }
    
    def is_user_eligible_for_918t(self, user_id):
        """
        Check if a user is eligible for 918T tokens
        
        Args:
            user_id (str): User ID
            
        Returns:
            bool: True if eligible, False otherwise
        """
        if user_id not in self.token_balances['users']:
            return False
            
        return self.token_balances['users'][user_id].get('918t_eligible', False)
    
    def select_reward_token_type(self, user_id, eth_amount):
        """
        Select the appropriate token type for a reward based on user eligibility and amount
        
        Args:
            user_id (str): User ID
            eth_amount (float): ETH equivalent amount
            
        Returns:
            str: Token type ('BBGT' or '918T')
        """
        # Check if user is eligible for 918T tokens
        is_918t_eligible = self.is_user_eligible_for_918t(user_id)
        
        # If eligible for 918T and amount is significant, use 918T
        if is_918t_eligible and eth_amount >= 0.05:  # Arbitrary threshold
            return '918T'
        else:
            # Otherwise use BBGT
            return 'BBGT'

# If run directly, show some token info
if __name__ == "__main__":
    rewards_system = TokenRewardsSystem(debug_mode=True)
    
    print("AI CEO Token Rewards System")
    print("==========================")
    
    print("\nToken Tiers:")
    for token_type, tier in rewards_system.TOKEN_TIERS.items():
        print(f"{token_type}: {tier['description']}")
        print(f"  Conversion Ratio: 1 ETH = {1 / tier['eth_conversion_ratio']} {token_type}")
        print(f"  Min/Max Amounts: {tier['min_amount']} - {tier['max_amount']} {token_type}")
    
    # Show some conversion examples
    print("\nConversion Examples:")
    eth_amount = 0.1  # 0.1 ETH
    
    bbgt_amount = rewards_system.convert_eth_to_token(eth_amount, 'BBGT')
    print(f"{eth_amount} ETH = {bbgt_amount} BBGT")
    
    t918_amount = rewards_system.convert_eth_to_token(eth_amount, '918T')
    print(f"{eth_amount} ETH = {t918_amount} 918T")
    
    # Simulate a reward
    user_id = "test_user"
    
    print("\nAwarding tokens to user:")
    result = rewards_system.award_tokens(
        user_id, 
        0.05,  # 0.05 ETH equivalent
        'BBGT',
        "Testing token rewards"
    )
    
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    if 'reward' in result:
        reward = result['reward']
        print(f"Tokens Awarded: {reward['token_amount']} {reward['token_type']}")
        print(f"ETH Equivalent: {reward['eth_equivalent']} ETH")
        print(f"Transaction Hash: {reward['transaction_hash']}")
    
    # Upgrade user and award 918T tokens
    print("\nUpgrading user to 918T eligibility:")
    upgrade_result = rewards_system.upgrade_user_to_918t(user_id)
    print(f"Upgrade result: {upgrade_result['message']}")
    
    print("\nAwarding 918T tokens to user:")
    result = rewards_system.award_tokens(
        user_id, 
        0.1,  # 0.1 ETH equivalent
        '918T',
        "Premium token reward"
    )
    
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    if 'reward' in result:
        reward = result['reward']
        print(f"Tokens Awarded: {reward['token_amount']} {reward['token_type']}")
        print(f"ETH Equivalent: {reward['eth_equivalent']} ETH")
        print(f"Transaction Hash: {reward['transaction_hash']}")
    
    # Show user balances
    print("\nUser Token Balances:")
    balances = rewards_system.get_user_token_balance(user_id)
    for token_type, amount in balances.items():
        if token_type in ['BBGT', '918T']:
            print(f"{token_type}: {amount}")
    
    # Show token stats
    print("\nToken Statistics:")
    stats = rewards_system.get_token_stats()
    
    print(f"BBGT in Circulation: {stats['bbgt_stats']['circulating_supply']}")
    print(f"918T in Circulation: {stats['918t_stats']['circulating_supply']}")
    print(f"Total Rewards: {stats['reward_stats']['total_rewards']}")
    print(f"Total ETH Equivalent: {stats['reward_stats']['total_eth_equivalent']} ETH")