"""Data loading and preprocessing utilities."""
from pathlib import Path
import pandas as pd
from typing import Tuple, List, Dict
from loguru import logger
import json
import yaml
import numpy as np
from rich.progress import Progress

class MovieDataLoader:
    def __init__(self, config_path: str | Path):
        """Initialize data loader with config."""
        self.config = self._load_config(config_path)
        self.cache_dir = Path(self.config.get('cache_dir', 'cache'))
        self.cache_dir.mkdir(exist_ok=True)
        
        # Set up data directories
        self.root_dir = Path(__file__).parent.parent.parent.parent
        self.data_dir = self.root_dir / 'data' / 'evals' / 'test_data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Local dataset path
        self.dataset_path = self.root_dir / 'ragtime-2-agentic' / 'data' / 'wiki_movie_plots_deduped_with_summaries.csv'

    def _load_config(self, config_path: str | Path) -> dict:
        """Load and validate configuration from YAML file."""
        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)
            
            # Validate required fields
            required_fields = ['models', 'metrics']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Missing required field in config: {field}")
            
            # Set default values if not present
            config.setdefault('batch_size', 32)
            config.setdefault('device', 'cpu')
            config.setdefault('max_length', 512)
            config.setdefault('cache_dir', 'cache')
            
            logger.info(f"Loaded configuration from {config_path}")
            return config
            
        except Exception as e:
            raise RuntimeError(f"Error loading config from {config_path}: {str(e)}")

    def load_dataset(self, force_download: bool = False) -> pd.DataFrame:
        """
        Load movie dataset with specified constraints.
        
        Args:
            force_download: If True, force reload even if cached version exists
        """
        cache_path = self.root_dir / 'data' / 'cache' / 'movie_dataset.parquet'
        
        # If not forcing download and cache exists, use cached version
        if not force_download and cache_path.exists():
            logger.info("Loading dataset from cache...")
            try:
                df = pd.read_parquet(cache_path)
                logger.info(f"Loaded {len(df)} movies from cache")
                return df
            except Exception as e:
                logger.warning(f"Error loading from cache: {str(e)}")
                logger.info("Attempting to load from local file...")
        
        try:
            # Load from local CSV file
            logger.info(f"Loading dataset from {self.dataset_path}")
            df = pd.read_csv(self.dataset_path)
            logger.info("Dataset loaded successfully")
            
            # Log column names to help debug
            logger.info(f"Available columns: {df.columns.tolist()}")
            
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            if cache_path.exists():
                logger.info("Attempting to load from cache as fallback...")
                df = pd.read_parquet(cache_path)
                return df
            else:
                raise RuntimeError(
                    f"Could not load dataset from {self.dataset_path} ({str(e)}) "
                    "and no cache found."
                )

        logger.info("Applying dataset filters...")
        # Apply constraints
        df = df[
            (df['Origin/Ethnicity'] == 'American') &
            (df['Release Year'] >= 1950)
        ]

        # Clean and preprocess
        logger.info("Preprocessing plot summaries...")
        # Just use the Plot field if Summary isn't available
        if 'Plot' in df.columns:
            if 'Summary' in df.columns:
                df['PlotSummary'] = df['Plot'].fillna('') + ' ' + df['Summary'].fillna('')
            else:
                df['PlotSummary'] = df['Plot'].fillna('')
                
        df['PlotSummary'] = df['PlotSummary'].str.strip()
        
        # Remove empty summaries
        df = df[df['PlotSummary'].str.len() > 0]

        # Cache the filtered dataset
        logger.info("Caching processed dataset...")
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_path)
        
        logger.info(f"Loaded {len(df)} movies after filtering")
        return df

    def prepare_test_data(self, progress: Progress = None) -> Path:
        """
        Prepare and save test data for evaluation.
        Returns path to test data file.
        """
        test_data_path = self.data_dir / 'movie_test_data.json'
        
        # Check if test data already exists
        if test_data_path.exists():
            logger.info(f"Test data already exists at {test_data_path}")
            return test_data_path
            
        task_id = None
        if progress:
            task_id = progress.add_task(
                "[cyan]Preparing test data...",
                total=4  # Number of main steps
            )
            
        # Load dataset
        logger.info("Loading movie dataset...")
        df = self.load_dataset()
        if progress and task_id:
            progress.advance(task_id)
            
        # Prepare evaluation samples
        logger.info("Preparing evaluation samples...")
        queries, documents, relevance_scores = self.prepare_evaluation_samples(
            df,
            n_samples=self.config.get('n_samples', 1000),
            n_queries=self.config.get('n_queries', 100)
        )
        if progress and task_id:
            progress.advance(task_id)
            
        # Prepare test data dictionary
        test_data = {
            'queries': queries,
            'documents': documents,
            'relevance_scores': relevance_scores,
            'metadata': {
                'n_samples': len(documents),
                'n_queries': len(queries),
                'creation_date': pd.Timestamp.now().isoformat()
            }
        }
        
        # Save test data
        logger.info(f"Saving test data to {test_data_path}")
        with open(test_data_path, 'w') as f:
            json.dump(test_data, f, indent=2)
        if progress and task_id:
            progress.advance(task_id)
            
        logger.info("Test data preparation complete!")
        if progress and task_id:
            progress.advance(task_id)
            
        return test_data_path

    def prepare_evaluation_samples(self, 
                                 df: pd.DataFrame, 
                                 n_samples: int = 1000,
                                 n_queries: int = 100) -> Tuple[List[str], List[str], List[List[int]]]:
        """Prepare evaluation samples from the dataset."""
        # Sample documents
        documents = df.sample(n_samples, random_state=42)['PlotSummary'].tolist()
        
        # Generate queries from random movies (not in documents)
        remaining_df = df[~df['PlotSummary'].isin(documents)]
        query_movies = remaining_df.sample(n_queries, random_state=42)
        
        # Create queries from movie titles and genres
        queries = [
            f"Movies similar to '{row['Title']}' ({row['Genre']})"
            for _, row in query_movies.iterrows()
        ]
        
        # Generate relevance scores
        relevance_scores = self._generate_relevance_scores(query_movies, documents, df)
        
        return queries, documents, relevance_scores

    def _generate_relevance_scores(self, 
                                 query_movies: pd.DataFrame, 
                                 documents: List[str], 
                                 full_df: pd.DataFrame) -> List[List[int]]:
        """Generate relevance scores based on genre similarity."""
        relevance_scores = []
        
        for _, query_movie in query_movies.iterrows():
            query_genre = set(query_movie['Genre'].split(','))
            
            # Find movies in documents and their genres
            doc_relevance = []
            for doc in documents:
                # Find the movie in full_df that matches this document
                movie_row = full_df[full_df['PlotSummary'] == doc].iloc[0]
                doc_genre = set(movie_row['Genre'].split(','))
                
                # Calculate genre overlap
                genre_overlap = len(query_genre & doc_genre) / len(query_genre | doc_genre)
                
                # Convert to binary relevance
                doc_relevance.append(1 if genre_overlap > 0.5 else 0)
            
            relevance_scores.append(doc_relevance)
        
        return relevance_scores
    
    def cache_embeddings(self, 
                        model_name: str, 
                        documents: List[str], 
                        embeddings: np.ndarray) -> None:
        """
        Cache embeddings for a model.
        
        Args:
            model_name: Name of the model used to generate embeddings
            documents: List of documents that were embedded
            embeddings: NumPy array of embeddings
        """
        # Create safe filename from model name
        safe_name = model_name.replace('/', '_')
        cache_path = self.cache_dir / f"{safe_name}_embeddings.npy"
        doc_path = self.cache_dir / f"{safe_name}_documents.json"

        # Save embeddings
        logger.info(f"Caching embeddings for {model_name}")
        np.save(cache_path, embeddings)
        
        # Save document mapping
        with open(doc_path, 'w') as f:
            json.dump(documents, f)
        
        logger.info(f"Cached {len(documents)} embeddings to {cache_path}")

    def load_cached_embeddings(self, 
                             model_name: str, 
                             documents: List[str]) -> np.ndarray | None:
        """
        Load cached embeddings if available and matching documents.
        
        Args:
            model_name: Name of the model to load embeddings for
            documents: List of documents to verify against cache
            
        Returns:
            NumPy array of embeddings if cache exists and matches, None otherwise
        """
        # Create safe filename from model name
        safe_name = model_name.replace('/', '_')
        cache_path = self.cache_dir / f"{safe_name}_embeddings.npy"
        doc_path = self.cache_dir / f"{safe_name}_documents.json"
        
        # Check if cache exists
        if not cache_path.exists() or not doc_path.exists():
            return None
            
        # Load and verify documents
        try:
            with open(doc_path) as f:
                cached_docs = json.load(f)
                
            # Check if documents match exactly
            if cached_docs == documents:
                logger.info(f"Found matching cache for {model_name}")
                embeddings = np.load(cache_path)
                logger.info(f"Loaded {len(embeddings)} embeddings from cache")
                return embeddings
            else:
                logger.info("Cache exists but documents don't match")
                return None
                
        except Exception as e:
            logger.warning(f"Error loading cache: {str(e)}")
            return None