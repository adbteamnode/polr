from web3 import Web3
from web3.exceptions import TransactionNotFound
from eth_utils import to_hex
from eth_utils import keccak, to_bytes
from eth_account import Account
from eth_account.messages import encode_defunct
from aiohttp import ClientResponseError, ClientSession, ClientTimeout, BasicAuth
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, random, time, json, uuid, re, os, pytz

wib = pytz.timezone('Asia/Jakarta')

POLARISE_TOPICS = {
    "core_protocol": [
        "ERC-1000: The Game-Changer NFT Standard",
        "NFT Liquidity Crisis: The Problem We're Solving",
        "Flash Trade Explained: Instant NFT Swaps",
        "P-Tokens: Your NFT's Liquid Twin"
    ],
    "defi_tools": [
        "100% LTV Loans: Too Good to Be True?",
        "Leverage in NFT Trading Without Getting Rekt",
        "Consignment: Get Paid Now, Sell Later",
        "Multi-Chain Strategy: Why It Matters"
    ],
    "nft_ecosystem": [
        "Beyond JPEGs: Real NFT Utility",
        "Non-Standard Assets (NSA) Market Explained",
        "NFT Gaming & Metaverse Integration",
        "Digital Art vs Financial Assets: The Debate"
    ],
    "platform": [
        "Polarise Testnet: Your First Steps",
        "From PawnFi to Polarise: The Rebrand Story",
        "Security First: How We Protect Your Assets",
        "User Experience Revolution in NFT DeFi"
    ],
    "insights": [
        "The NFT Market: Dead or Just Getting Started?",
        "DeFi + NFTs: Why It Took So Long",
        "Institutional Money & NFT Liquidity",
        "Web3's Biggest Lie: You Own Your Assets"
    ],
    "market_analysis": [
        "NFT Floor Price Dynamics Explained",
        "Volatility: Friend or Foe in NFT Markets?",
        "The Liquidity Premium: Why It Matters",
        "Market Cycles & Timing Your NFT Strategy"
    ],
    "educational": [
        "NFT Liquidity 101: A Beginner's Guide",
        "Smart Contracts Demystified for Normies",
        "Tokenomics: The $PFT Guide",
        "Risk Management for NFT Holders"
    ],
    "future_vision": [
        "The Next Evolution of NFTs",
        "Building the Future of Digital Ownership"
    ],
    "hot_takes": [
        "OpenSea is Dead (And That's Good)",
        "Why Most NFT Projects Deserve to Fail",
        "The Truth About NFT Communities",
        "Royalties Are Killing NFTs",
        "DAOs Don't Work (Yet)",
        "The Metaverse Hype Was a Lie",
        "Why I'm Bullish on NFTs But Bearish on Your Project",
        "The Real Reason You Can't Sell Your NFT",
        "Crypto Twitter Is Ruining Crypto",
        "If You Don't Understand Liquidity, You Don't Understand NFTs"
    ]
}

COMMENT_LIST = [
    "Good", "Great", "Nice", "Awesome", "Cool", "Well done", "Good job", "Solid", "Perfect", "Amazing",
    "GM", "GM Mate", "Good Morning", "Morning Mate", "Morning all", "GM everyone", "Rise and shine", "Morning vibes", "Fresh start", "New day",
    "GN", "GN Mate", "Good Night", "Night Mate", "Sleep well", "Sweet dreams", "Rest well", "Night vibes", "Time to rest", "See you tomorrow",
    "Hello", "Hello Mate", "Hi", "Hi Mate", "Hey", "Hey Mate", "Yo", "Yo Mate", "What's up", "Sup Mate",
    "Agree", "Totally agree", "Absolutely", "Indeed", "Exactly", "True", "Well said", "Makes sense", "Facts", "100% agree",
    "LFG", "Let's go", "Keep going", "On fire", "Bullish", "WAGMI", "To the moon", "Big vibes", "Strong move", "Nice play",
    "Follow me", "Follow back", "Let's connect", "Support each other", "Stay connected", "See you around", "Much respect", "Cheers", "Salute", "Respect"
]

class Polarise:
    def __init__(self) -> None:
        self.BASE_API = "https://apia.polarise.org/api/app/v1"
        self.RPC_URL = "https://chainrpc.polarise.org/"
        self.EXPLORER = "https://explorer.polarise.org/tx/"
        self.REF_CODE = "fHqx2G" # U can change it with yours.

        self.CONFIG = {
            "transfer": {
                "amount": 0.001,
                "gas_fee": 0.0021,
                "recepient": "0x9c4324156bA59a70FFbc67b98eE2EF45AEE4e19F"
            },
            "donate": {
                "amount": 1,
                "recepient": "0x1d1afc2d015963017bed1de13e4ed6c3d3ed1618",
                "token_address": "0x351EF49f811776a3eE26f3A1fBc202915B8f2945",
                "contract_address": "0x639A8A05DAD556256046709317c76927b053a85D",
            },
            "discussion": {
                "contract_address": "0x58477a0e15ae82E9839f209b13EFF25eC06c252B",
            }
        }

        self.CONTRACT_ABI = [
            {
                "inputs": [
                    { "internalType": "address", "name": "account", "type": "address" }
                ],
                "name": "balanceOf",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "owner", "type": "address" },
                    { "internalType": "address", "name": "spender", "type": "address" }
                ],
                "name": "allowance",
                "outputs": [
                    { "internalType": "uint256", "name": "", "type": "uint256" }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    { "internalType": "address", "name": "spender", "type": "address" },
                    { "internalType": "uint256", "name": "value", "type": "uint256" }
                ],
                "name": "approve",
                "outputs": [
                    { "internalType": "bool", "name": "", "type": "bool" }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    { "name": "receiver", "type": "address", "internalType": "address"}, 
                    { "name": "amount", "type": "uint256", "internalType": "uint256"}
                ],
                "name": "donate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "type": "function",
                "name": "createDiscussionEvent",
                "inputs": [
                    { "name": "questionId", "type": "bytes32", "internalType": "bytes32" }, 
                    { "name": "nftMint", "type": "bool", "internalType": "bool" }, 
                    { "name": "communityRecipient", "type": "address", "internalType": "address" }, 
                    { "name": "collateralToken", "type": "address", "internalType": "address" }, 
                    { "name": "endTime", "type": "uint64", "internalType": "uint64" }, 
                    { "name": "outcomeSlots", "type": "bytes32[]", "internalType": "bytes32[]" }
                ],
                "outputs": [],
                "stateMutability": "nonpayable"
            }
        ]

        self.HEADERS = {}
        self.api_key = None
        self.all_topics = []
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.auth_tokens = {}
        self.nonce = {}
        self.sub_id = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Polarise{Fore.BLUE + Style.BRIGHT} Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_all_topics(self):
        try:
            all_topics = []
            for category, topics in POLARISE_TOPICS.items():
                all_topics.extend(topics)
            return all_topics
        except Exception as e:
            return []
        
    def load_accounts(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            return accounts
        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return []
        
    def load_grok_api_key(self):
        try:
            with open('grok_api_key.txt', 'r') as file:
                grok_api_key = file.readline().strip()
            return grok_api_key
        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'grok_api_key.txt' Not Found.{Style.RESET_ALL}")
            return []
    
    def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, token):
        if token not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[token] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[token]

    def rotate_proxy_for_account(self, token):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[token] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
    
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address
            
            return address
        except Exception as e:
            return None
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None
        
    def generate_signature(self, account: str, address: str):
        try:
            message = f"Nonce to confirm: {self.nonce[address]}"
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            return message, signature
        except Exception as e:
            raise Exception(f"Generate Signature Failed: {str(e)}")
        
    def generate_login_payload(self, account: str, address: str):
        try:
            message, signature = self.generate_signature(account, address)
            payload = {
                "signature": signature,
                "chain_name": "polarise",
                "name": address[:6],
                "nonce": self.nonce[address],
                "wallet": address,
                "sid": self.access_tokens[address],
                "sub_id": self.sub_id[address],
                "inviter_code": self.REF_CODE
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Login Payload Failed: {str(e)}")
        
    def generate_swap_payload(self, account: str, address: str, user_id: int, username: str, used_points: int):
        try:
            message, signature = self.generate_signature(account, address)
            payload = {
                "user_id": user_id,
                "user_name": username,
                "user_wallet": address,
                "used_points": used_points,
                "token_symbol": "GRISE",
                "chain_name": "polarise",
                "signature": signature,
                "sign_msg": message
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Swap Points Payload Failed: {str(e)}")
        
    def generate_save_post_payload(self, user_id: str, content: dict):
        try:
            payload = {
                "user_id": user_id,
                "chain_name": "polarise",
                "community_id": 0,
                "community_name": "",
                "title": content["title"],
                "tags": [],
                "description": content["description"],
                "published_time": int(time.time()) * 1000,
                "media_links": "[]",
                "is_subscribe_enable": False
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Save Post Payload Failed: {str(e)}")
        
    def generate_discuss_options(self):
        options = [
            {"index":0,"title":"Agree","price":0,"total_buy_share":0,"total_sell_share":0,"total_held_share":0},
            {"index":1,"title":"Not Agree","price":0,"total_buy_share":0,"total_sell_share":0,"total_held_share":0}
        ]

        return options
    
    def build_outcome_slots(self, options: list):
        outcome_slots = []
        for opt in options:
            if not isinstance(opt, dict):
                raise ValueError("each option must be dict")

            title = opt.get("title")
            if not title or not isinstance(title, str):
                raise ValueError("option.title must be string")

            hashed = keccak(to_bytes(text=title))
            outcome_slots.append("0x" + hashed.hex())

        return outcome_slots

    def generate_save_discussion_payload(self, user_id: str, discuss_data: dict):
        try:
            payload = {
                "user_id": user_id,
                "community_id": 0,
                "community_name": "",
                "title": discuss_data['title'],
                "options": json.dumps(discuss_data['options']),
                "tags": [],
                "description": discuss_data["description"],
                "published_time": discuss_data['published_time'],
                "tx_hash": discuss_data['tx_hash'],
                "chain_name": "polarise",
                "media_links": "[]",
                "question_id": discuss_data['question_id'],
                "end_time": discuss_data['end_time']
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Save Discussion Payload Failed: {str(e)}")
    
    async def get_web3_with_check(self, address: str, use_proxy: bool, retries=3, timeout=60):
        request_kwargs = {"timeout": timeout}

        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        if use_proxy and proxy:
            request_kwargs["proxies"] = {"http": proxy, "https": proxy}

        for attempt in range(retries):
            try:
                web3 = Web3(Web3.HTTPProvider(self.RPC_URL, request_kwargs=request_kwargs))
                web3.eth.get_block_number()
                return web3
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                raise Exception(f"Failed to Connect to RPC: {str(e)}")
        
    async def get_token_balance(self, address: str, use_proxy: bool, token_address=None):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            if token_address is None:
                balance = web3.eth.get_balance(address)
            else:
                asset_address = web3.to_checksum_address(token_address)
                token_contract = web3.eth.contract(address=asset_address, abi=self.CONTRACT_ABI)
                balance = token_contract.functions.balanceOf(address).call()

            token_balance = web3.from_wei(balance, "ether")

            return token_balance
        except Exception as e:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
            )
            return None
        
    async def send_raw_transaction_with_retries(self, account, web3, tx, retries=5):
        for attempt in range(retries):
            try:
                signed_tx = web3.eth.account.sign_transaction(tx, account)
                raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash = web3.to_hex(raw_tx)
                return tx_hash
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.BLUE + Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}[Attempt {attempt + 1}] Send TX Error: {str(e)}{Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Hash Not Found After Maximum Retries")

    async def wait_for_receipt_with_retries(self, web3, tx_hash, retries=5):
        for attempt in range(retries):
            try:
                receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
                return receipt
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.BLUE + Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}[Attempt {attempt + 1}] Wait for Receipt Error: {str(e)}{Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Receipt Not Found After Maximum Retries")

    async def perform_transfer(self, account: str, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            amount_to_wei = web3.to_wei(self.CONFIG['transfer']['amount'], "ether")

            max_priority_fee = web3.to_wei(100, "gwei")
            max_fee = max_priority_fee

            transfer_tx = {
                "from": web3.to_checksum_address(address),
                "to": web3.to_checksum_address(self.CONFIG['transfer']['recepient']),
                "value": amount_to_wei,
                "gas": 21000,
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            }

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, transfer_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber

            return amount_to_wei, tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.BLUE + Style.BRIGHT}   Message : {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
            )
            return None, None, None
        
    async def approving_token(self, account: str, address: str, spender: str, asset_address: str, amount: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)
            
            token_contract = web3.eth.contract(address=asset_address, abi=self.CONTRACT_ABI)

            allowance = token_contract.functions.allowance(address, spender).call()
            if allowance < amount:
                approve_data = token_contract.functions.approve(spender, 2**256 - 1)
                estimated_gas = approve_data.estimate_gas({"from": address})

                max_priority_fee = web3.to_wei(100, "gwei")
                max_fee = max_priority_fee

                approve_tx = approve_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": web3.eth.get_transaction_count(address, "pending"),
                    "chainId": web3.eth.chain_id,
                })

                tx_hash = await self.send_raw_transaction_with_retries(account, web3, approve_tx)
                receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                block_number = receipt.blockNumber

                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Approve : {Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Block   : {Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT}{block_number}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Tx Hash : {Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT}{tx_hash}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Explorer: {Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT}{self.EXPLORER}{tx_hash}{Style.RESET_ALL}"
                )
                await asyncio.sleep(3)

            return True
        except Exception as e:
            raise Exception(f"Approving Token Contract Failed: {str(e)}")

    async def perform_donate(self, account: str, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            amount_to_wei = web3.to_wei(self.CONFIG['donate']['amount'], "ether")

            receiver_address = web3.to_checksum_address(self.CONFIG['donate']['recepient'])
            token_address = web3.to_checksum_address(self.CONFIG['donate']['token_address'])
            contract_address = web3.to_checksum_address(self.CONFIG['donate']['contract_address'])

            await self.approving_token(account, address, contract_address, token_address, amount_to_wei, use_proxy)

            token_contract = web3.eth.contract(address=contract_address, abi=self.CONTRACT_ABI)
            donate_data = token_contract.functions.donate(receiver_address, amount_to_wei)
            estimated_gas = donate_data.estimate_gas({"from": address})

            max_priority_fee = web3.to_wei(100, "gwei")
            max_fee = max_priority_fee

            donate_tx = donate_data.build_transaction({
                "from": address,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, donate_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.BLUE + Style.BRIGHT}   Message : {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
            )
            return None, None

    async def perform_create_discuss(self, account: str, address: str, discuss_data: dict, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            community_recipient = "0x0000000000000000000000000000000000000000"
            collateral_token = web3.to_checksum_address(self.CONFIG['donate']['token_address'])
            contract_address = web3.to_checksum_address(self.CONFIG['discussion']['contract_address'])

            question_id = "0x" + discuss_data['question_id']
            end_time = discuss_data['end_time']

            outcome_slots = self.build_outcome_slots(discuss_data['options'])

            token_contract = web3.eth.contract(address=contract_address, abi=self.CONTRACT_ABI)
            discuss_data = token_contract.functions.createDiscussionEvent(
                question_id, False, community_recipient, collateral_token, end_time, outcome_slots
            )
            estimated_gas = discuss_data.estimate_gas({"from": address})

            max_priority_fee = web3.to_wei(100, "gwei")
            max_fee = max_priority_fee

            discuss_tx = discuss_data.build_transaction({
                "from": address,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, discuss_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.BLUE + Style.BRIGHT}   Message : {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
            )
            return None, None
        
    async def generate_extra_info(self, account: str, address: str, use_proxy: bool):
        amount, tx_hash, block_number = await self.perform_transfer(account, address, use_proxy)
        if amount and tx_hash and block_number:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Donate  : {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Block   : {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{block_number}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Tx Hash : {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{tx_hash}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Explorer: {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{self.EXPLORER}{tx_hash}{Style.RESET_ALL}"
            )
            
            extra_dict = {
                "tx_hash": tx_hash,
                "from": address,
                "to": self.CONFIG['transfer']["recepient"],
                "value": str(amount)
            }

            extra = json.dumps(extra_dict)
            
            await asyncio.sleep(3)
            return extra
        else:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT}Perform On-Chain Failed{Style.RESET_ALL}"
            )
            return False
        
    async def process_perfrom_donate(self, account: str, address: str, use_proxy: bool):
        tx_hash, block_number = await self.perform_donate(account, address, use_proxy)
        if tx_hash and block_number:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}                                     "
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Block   : {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{block_number}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Tx Hash : {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{tx_hash}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Explorer: {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{self.EXPLORER}{tx_hash}{Style.RESET_ALL}"
            )

            await asyncio.sleep(3)
            return True
        else:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT}Perform On-Chain Failed{Style.RESET_ALL}"
            )
            return False
        
    async def process_perfrom_create_discuss(self, account: str, address: str, discuss_data: dict, use_proxy: bool):
        tx_hash, block_number = await self.perform_create_discuss(account, address, discuss_data, use_proxy)
        if tx_hash and block_number:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}                                     "
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Block   : {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{block_number}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Tx Hash : {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{tx_hash}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Explorer: {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{self.EXPLORER}{tx_hash}{Style.RESET_ALL}"
            )

            await asyncio.sleep(3)
            return tx_hash
        else:
            self.log(
                f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT}Perform On-Chain Failed{Style.RESET_ALL}"
            )
            return False
        
    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run Without Proxy{Style.RESET_ALL}")
                proxy_choice = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        "With" if proxy_choice == 1 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        rotate_proxy = False
        if proxy_choice == 1:
            while True:
                rotate_proxy = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate_proxy in ["y", "n"]:
                    rotate_proxy = rotate_proxy == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return proxy_choice, rotate_proxy
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=10)) as session:
                async with session.get(url="https://api.ipify.org?format=json", proxy=proxy, proxy_auth=proxy_auth) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Not 200 OK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
        
    async def get_nonce(self, address: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/profile/getnonce"
        data = json.dumps({"wallet": address, "chain_name": "polarise"})
        headers = {
            **self.HEADERS[address],
            "Authorization": "Bearer",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Get Nonce Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
        
    async def gen_biz_id(self, address: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/discussion/generatebizid"
        data = json.dumps({
            "biz_input": address, 
            "biz_type": "subscription_question", 
            "chain_name": "polarise"
        })
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": "Bearer",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Generate Biz Id Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
        
    async def wallet_login(self, account: str, address: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/profile/login"
        data = json.dumps(self.generate_login_payload(account, address))
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": "Bearer",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
        
    async def profile_info(self, address: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/profile/profileinfo"
        data = json.dumps({"chain_name": "polarise"})
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Profile  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Fetch Info Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
        
    async def swap_points(self, account: str, address: str, user_id: int, username: str, used_points: int, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/profile/swappoints"
        data = json.dumps(self.generate_swap_payload(account, address, user_id, username, used_points))
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Swap     :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
        
    async def task_list(self, address: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/points/tasklist"
        data = json.dumps({"user_wallet": address, "chain_name": "polarise"})
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Task List:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Fetch List Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
        
    async def generate_content(self, topic: str, api_key: str, retries=5):
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": "llama-3.3-70b-versatile",
            "temperature": 1.0,
            "max_tokens": 300,
            "top_p": 0.95,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a passionate content creator and 'yapper' for Polarise Protocol (a pioneering NFT liquidity initiator reshaping NFT finance with all-in-one system). "
                        "Your mission: spark conversations, challenge perspectives, and make people THINK.\n\n"
                        
                        "TONE & STYLE:\n"
                        "- Ultra conversational, like you're texting a friend\n"
                        "- High energy but authentic—no fake hype\n"
                        "- Opinionated but open to dialogue\n"
                        "- Mix of punchy one-liners and thought-provoking questions\n"
                        "- Use analogies, pop culture refs, real-life examples\n\n"
                        
                        "FORMATTING:\n"
                        "- Short paragraphs (1-3 sentences max)\n"
                        "- Strategic line breaks for impact\n"
                        "- Occasional emojis (don't overdo it) 🔥💡✨\n"
                        "- CAPS for emphasis on key points\n"
                        "- Rhetorical questions to hook readers\n\n"
                        
                        "CONTENT APPROACH:\n"
                        "- Start with a HOOK (question, hot take, or relatable scenario)\n"
                        "- Present polarizing/thought-provoking angles\n"
                        "- Back up claims with logic or examples\n"
                        "- End with a call-to-action or lingering question\n"
                        "- Make readers feel seen, challenged, or inspired\n\n"
                        
                        "AVOID:\n"
                        "- Corporate buzzwords or jargon\n"
                        "- Being preachy or condescending\n"
                        "- Generic inspirational quotes\n"
                        "- Over-explaining (trust your audience)\n\n"
                        
                        "You must ALWAYS respond with valid JSON in this exact format:\n"
                        "{\n"
                        '  "title": "Your catchy title here",\n'
                        '  "content": "Your engaging content here"\n'
                        "}\n\n"
                        
                        "Write in English. Be bold, be real, be memorable."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Create a yapper-style post about: {topic}\n\n"
                        "Generate:\n"
                        "1. TITLE: Catchy, attention-grabbing, 5-12 words max. Make it clickable!\n"
                        "2. CONTENT: Engaging short-form content (100-200 words) that:\n"
                        "   - Grabs attention immediately\n"
                        "   - Presents a fresh or controversial perspective\n"
                        "   - Makes people want to comment/share/debate\n"
                        "   - Aligns with polarise.org's mission\n\n"
                        
                        "Respond ONLY with valid JSON. No markdown, no code blocks, no explanations. "
                        "Just pure JSON with 'title' and 'content' keys."
                    )
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json=payload) as response:
                        data = await response.json()
                        if response.status == 429:
                            err_msg = data.get("error", {}).get("message", "Unknown Error")

                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Create Content Failed{Style.RESET_ALL}"
                            )
                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                            )
                            return None
                        
                        response.raise_for_status()

                        raw_content = data["choices"][0]["message"]["content"].strip()
        
                        if raw_content.startswith("```json"):
                            raw_content = raw_content.replace("```json", "").replace("```", "").strip()
                        elif raw_content.startswith("```"):
                            raw_content = raw_content.replace("```", "").strip()
                        
                        result = json.loads(raw_content)
                        
                        if "title" not in result or "content" not in result:
                            raise ValueError("Response missing 'title' or 'content' field")
                        
                        return {
                            "title": result["title"].strip(),
                            "description": result["content"].strip(),
                            "topic": topic
                        }
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}Create Content Failed{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                return None
            
    async def gen_question_id(self, address: str, biz_input: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/discussion/generatebizid"
        data = json.dumps({
            "biz_input": biz_input,
            "biz_type": "discussion_question",
            "chain_name": "polarise"
        })
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": "Bearer",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}Generate Question Id Failed{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                return None
        
    async def save_discussion(self, address: str, user_id: int, discuss_data: dict, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/discussion/savediscussion"
        data = json.dumps(self.generate_save_discussion_payload(user_id, discuss_data))
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Post    : {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                return None
        
    async def save_post(self, address: str, user_id: int, content: dict, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/posts/savepost"
        data = json.dumps(self.generate_save_post_payload(user_id, content))
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Post    : {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                return None
        
    async def home_list(self, address: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/aggregation/homelist"
        data = json.dumps({"user_id": 0, "cursor": 0, "limit": 20, "chain_name": "polarise"})
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}Failed to Fetch Post List{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                return None
        
    async def save_comment(self, address: str, user_id: int, post_id: int, content: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/posts/savecomment"
        data = json.dumps({
            "user_id": user_id, 
            "post_id": post_id, 
            "content": content,
            "tags" : [],
            "published_time": int(time.time()) * 1000,
            "chain_name": "polarise"
        })
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Comment : {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                return None
        
    async def save_suborder(self, address: str, sub_address: str, use_proxy: bool, retries=5):
        url = f"{self.BASE_API}/subscription/savesuborder"
        data = json.dumps({
            "subed_addr": sub_address, 
            "sub_id": self.sub_id[address],
            "order_time": int(time.time()),
            "chain_name": "polarise"
        })
        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Suborder: {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                return None
        
    async def complete_task(self, address: str, task_id: int, title: str, use_proxy: bool, extra=None, retries=5):
        url = f"{self.BASE_API}/points/completetask"
        payload = {
            "user_wallet": address, 
            "task_id": task_id, 
            "chain_name": "polarise"
        }
        
        if extra is not None:
            payload["extra_info"] = extra

        data = json.dumps(payload)

        headers = {
            **self.HEADERS[address],
            "Accesstoken": self.access_tokens[address],
            "Authorization": f"Bearer {self.auth_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            proxy_url = self.get_next_proxy_for_account(address) if use_proxy else None
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                if task_id in [3, 4, 5, 6]:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Not Completed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                    )
                return None
            
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy    :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(proxy)
            if is_valid: return True

            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)
                await asyncio.sleep(1)
                continue

            return False
        
    async def process_wallet_login(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
       is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
       if is_valid:
            
            get_nonce = await self.get_nonce(address, use_proxy)
            if not get_nonce: return False

            if get_nonce.get("code") != "200":
                err_msg = get_nonce.get("msg", "Unknown Error")
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Get Nonce Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                )
                return False
            
            self.nonce[address] = get_nonce.get("signed_nonce")
            
            biz_id = await self.gen_biz_id(address, use_proxy)
            if not biz_id: return False

            if biz_id.get("code") != "200":
                err_msg = biz_id.get("msg", "Unknown Error")
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Generate Biz Id Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                )
                return False
            
            self.sub_id[address] = biz_id.get("data", {}).get("Biz_Id")

            login = await self.wallet_login(account, address, use_proxy)
            if not login: return False

            if login.get("code") != "200":
                err_msg = login.get("msg", "Unknown Error")
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                )
                return False

            auth_token = login.get("data", {}).get("auth_token_info", {}).get("auth_token")
            self.auth_tokens[address] = f"{auth_token} {self.access_tokens[address]} {address} polarise"

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status   :{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
            )
            return True
    
    async def process_accounts(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        logined = await self.process_wallet_login(account, address, use_proxy, rotate_proxy)
        if logined:
            
            profile = await self.profile_info(address, use_proxy)
            if profile:

                if profile.get("code") == "200":
                    user_id = profile.get("data", {}).get("id")
                    username = profile.get("data", {}).get("user_name")
                    exchange_points = profile.get("data", {}).get("exchange_total_points")
                    cumulative_revenue = profile.get("data", {}).get("cumulative_revenue")

                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Points   :{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {exchange_points} Points {Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Balance  :{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {cumulative_revenue} GRISE {Style.RESET_ALL}"
                    )

                    if exchange_points >= 100:
                        # Modified logic: Get 100 max even if points are higher
                        used_points = 100

                        swap = await self.swap_points(account, address, user_id, username, used_points, use_proxy)
                        if swap:

                            if swap.get("code") == "200":
                                self.log(f"{Fore.CYAN+Style.BRIGHT}Swap     :{Style.RESET_ALL}")

                                received_amount = swap.get("data", {}).get("received_amount")
                                tx_hash = swap.get("data", {}).get("tx_hash")
                                
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Received: {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{received_amount} GRISE{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Tx Hash : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{tx_hash}{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Explorer: {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{self.EXPLORER}{tx_hash}{Style.RESET_ALL}"
                                )

                            else:
                                err_msg = swap.get("msg", "Unknown Error")
                                self.log(
                                    f"{Fore.CYAN+Style.BRIGHT}Swap     :{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                                )

                    else:
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}Swap     :{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Insufficient Points, must >= 100 {Style.RESET_ALL}"
                        )

                else:
                    err_msg = profile.get("msg", "Unknown Error")
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Profile  :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Fetch Info Failed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                    )

            task_list = await self.task_list(address, use_proxy)
            if task_list:

                if task_list.get("code") == "200":
                    self.log(f"{Fore.CYAN+Style.BRIGHT}Task List:{Style.RESET_ALL}")

                    tasks = task_list.get("data", {}).get("list")
                    for task in tasks:
                        task_id = task.get("id")
                        title = task.get("name")
                        reward = task.get("points")
                        state = task.get("state")

                        if state == 1:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} Already Completed {Style.RESET_ALL}"
                            )
                            continue

                        if task_id == 3:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} Skipped {Style.RESET_ALL}"
                            )
                            continue

                        elif task_id in [1, 2]:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                            )

                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Amount  : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{self.CONFIG['transfer']['amount']} POLAR{Style.RESET_ALL}"
                            )
                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Gas Fee : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{self.CONFIG['transfer']['gas_fee']} POLAR{Style.RESET_ALL}"
                            )

                            balance = await self.get_token_balance(address, use_proxy)
                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Balance : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{balance} POLAR{Style.RESET_ALL}"
                            )

                            if balance is None:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Failed to Fetch POLAR Token Balance{Style.RESET_ALL}"
                                )
                                continue

                            if balance < self.CONFIG['transfer']['amount'] + self.CONFIG['transfer']['gas_fee']:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Insufficient POLAR Token Balance{Style.RESET_ALL}"
                                )
                                continue

                            extra = await self.generate_extra_info(account, address, use_proxy)
                            if not extra: continue

                            complete = await self.complete_task(address, task_id, title, use_proxy, extra)
                            if not complete: continue

                            if complete.get("code") != "200":
                                err_msg = complete.get("msg", "Unknown Error")
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                )
                                continue

                            if complete.get("data", {}).get("finish_status") == 1:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Reward  : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{reward} Points{Style.RESET_ALL}"
                                )
                            elif complete.get("data", {}).get("finish_status") == 0:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}Already Completed{Style.RESET_ALL}"
                                )

                        elif task_id in [7, 8]:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                            )

                            if not self.api_key:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Grok Api Key Not Found{Style.RESET_ALL}"
                                )
                                continue

                            topic = random.choice(self.all_topics)

                            if not topic:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Topic Not Found{Style.RESET_ALL}"
                                )
                                continue

                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Topic   : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{topic}{Style.RESET_ALL}"
                            )

                            content = await self.generate_content(topic, self.api_key)
                            if not content: continue

                            title = content['title']
                            description = content['description']

                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Title   : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                            )
                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Content : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{description}{Style.RESET_ALL}"
                            )

                            if task_id == 7:
                                timestamp = int(time.time()) * 1000
                                biz_input = f"{title.lower()}{timestamp}-agree-not agree"

                                biz_id = await self.gen_question_id(address, biz_input, use_proxy)
                                if not biz_id: continue
                        
                                if biz_id.get("code") != "200":
                                    err_msg = biz_id.get("msg", "Unknown Error")
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Generate Question Id Failed{Style.RESET_ALL}"
                                    )
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                    )
                                    continue

                                question_id = biz_id.get("data", {}).get("Biz_Id")

                                options = self.generate_discuss_options()

                                now_time = int(time.time())
                                published_time = now_time * 1000
                                end_time = now_time + 1209600

                                discuss_data = {
                                    "title": title,
                                    "description": description,
                                    "question_id": question_id,
                                    "options": options,
                                    "published_time": published_time,
                                    "end_time": end_time,
                                }

                                tx_hash = await self.process_perfrom_create_discuss(account, address, discuss_data, use_proxy)
                                if not tx_hash: continue

                                discuss_data["tx_hash"] = tx_hash

                                save_discuss = await self.save_discussion(address, user_id, discuss_data, use_proxy)
                                if not save_discuss: continue

                                if save_discuss.get("code") != "200":
                                    err_msg = save_discuss.get("msg", "Unknown Error")
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Post    : {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                                    )
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                    )
                                    continue

                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Post    : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}"
                                )

                            elif task_id == 8:
                                save_post = await self.save_post(address, user_id, content, use_proxy)
                                if not save_post: continue

                                if save_post.get("code") != "200":
                                    err_msg = save_post.get("msg", "Unknown Error")
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Post    : {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                                    )
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                    )
                                    continue

                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Post    : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}"
                                )

                            complete = await self.complete_task(address, task_id, title, use_proxy)
                            if not complete: continue

                            if complete.get("code") != "200":
                                err_msg = complete.get("msg", "Unknown Error")
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                )
                                continue

                            if complete.get("data", {}).get("finish_status") == 1:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Reward  : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{reward} Points{Style.RESET_ALL}"
                                )
                            elif complete.get("data", {}).get("finish_status") == 0:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}Already Completed{Style.RESET_ALL}"
                                )

                        elif task_id == 9:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                            )

                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Amount  : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{self.CONFIG['donate']['amount']} GRISE{Style.RESET_ALL}"
                            )

                            balance = await self.get_token_balance(address, use_proxy, self.CONFIG['donate']['token_address'])
                            self.log(
                                f"{Fore.BLUE+Style.BRIGHT}   Balance : {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{balance} GRISE{Style.RESET_ALL}"
                            )

                            if balance is None:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Failed to Fetch GRISE Token Balance{Style.RESET_ALL}"
                                )
                                continue

                            if balance < self.CONFIG['donate']['amount']:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Insufficient GRISE Token Balance{Style.RESET_ALL}"
                                )
                                continue

                            donate = await self.process_perfrom_donate(account, address, use_proxy)
                            if not donate: continue

                            complete = await self.complete_task(address, task_id, title, use_proxy)
                            if not complete: continue

                            if complete.get("code") != "200":
                                err_msg = complete.get("msg", "Unknown Error")
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                )
                                continue

                            if complete.get("data", {}).get("finish_status") == 1:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Reward  : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{reward} Points{Style.RESET_ALL}"
                                )
                            elif complete.get("data", {}).get("finish_status") == 0:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}Already Completed{Style.RESET_ALL}"
                                )

                        elif task_id in [10, 11]:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                            )

                            home_list = await self.home_list(address, use_proxy)
                            if not home_list: continue

                            if home_list.get("code") != "200": 
                                err_msg = home_list.get("msg", "Unknown Error")
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Failed to Fetch Post List{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                )
                                continue

                            post = home_list.get("data", {}).get("list", [])
                            square = random.choice(post)

                            post_id = square.get("id")
                            sub_address = square.get("user_wallet")

                            if task_id == 10:
                                content = random.choice(COMMENT_LIST)

                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Post Id : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{post_id}{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Content : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{content}{Style.RESET_ALL}"
                                )

                                save_comment = await self.save_comment(address, user_id, post_id, content, use_proxy)
                                if not save_comment: continue

                                if save_comment.get("code") != "200":
                                    err_msg = save_comment.get("msg", "Unknown Error")
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Comment : {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                                    )
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                    )
                                    continue

                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Comment : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}"
                                )
                                
                            elif task_id == 11:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Address : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{sub_address}{Style.RESET_ALL}"
                                )

                                save_suborder = await self.save_suborder(address, sub_address, use_proxy)
                                if not save_suborder: continue

                                if save_suborder.get("code") != "200":
                                    err_msg = save_suborder.get("msg", "Unknown Error")
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Suborder: {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                                    )
                                    self.log(
                                        f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                    )
                                    continue

                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Suborder: {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Success{Style.RESET_ALL}"
                                )

                            complete = await self.complete_task(address, task_id, title, use_proxy)
                            if not complete: continue

                            if complete.get("code") != "200":
                                err_msg = complete.get("msg", "Unknown Error")
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Message : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}{err_msg}{Style.RESET_ALL}"
                                )
                                continue

                            if complete.get("data", {}).get("finish_status") == 1:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Completed{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Reward  : {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{reward} Points{Style.RESET_ALL}"
                                )
                            elif complete.get("data", {}).get("finish_status") == 0:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.BLUE+Style.BRIGHT}   Status  : {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}Already Completed{Style.RESET_ALL}"
                                )

                        else:
                            complete = await self.complete_task(address, task_id, title, use_proxy)
                            if not complete: continue

                            if complete.get("code") != "200":
                                err_msg = complete.get("msg", "Unknown Error")
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Not Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                                )
                                continue

                            if complete.get("data", {}).get("finish_status") == 1:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.CYAN+Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{reward} Points{Style.RESET_ALL}"
                                )
                            elif complete.get("data", {}).get("finish_status") == 0:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Not Completed {Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} Already Completed {Style.RESET_ALL}"
                                )

                else:
                    err_msg = task_list.get("msg", "Unknown Error")
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Task List:{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Fetch List Failed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                    )
            
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts: 
                self.log(f"{Fore.RED+Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
                return

            self.api_key = self.load_grok_api_key()
            self.all_topics = self.load_all_topics()
            
            proxy_choice, rotate_proxy = self.print_question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                use_proxy = True if proxy_choice == 1 else False
                if use_proxy: self.load_proxies()
                
                separator = "=" * 25
                for idx, account in enumerate(accounts, start=1):
                    if account:
                        address = self.generate_address(account)

                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {idx} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )

                        if not address:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}Status   :{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            )
                            continue

                        self.access_tokens[address] = str(uuid.uuid4())

                        self.HEADERS[address] = {
                            "Accept": "*/*",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Origin": "[https://app.polarise.org](https://app.polarise.org)",
                            "Referer": "[https://app.polarise.org/](https://app.polarise.org/)",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-site",
                            "User-Agent": FakeUserAgent().random
                        }

                        await self.process_accounts(account, address, use_proxy, rotate_proxy)
                        await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                seconds = 24 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1
        
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Polarise()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Polarise - BOT{Style.RESET_ALL}                                        "                             
        )
