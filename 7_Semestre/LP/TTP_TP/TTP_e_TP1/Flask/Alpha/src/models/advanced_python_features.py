"""
Módulo demonstrando características avançadas do Python.
Aplica decoradores, context managers, metaclasses e outros recursos avançados.
"""

import functools
import time
import logging
from contextlib import contextmanager
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum, auto


# Enum para demonstrar uso de enumerações
class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


# Decorador personalizado para medir tempo de execução
def measure_time(func: Callable) -> Callable:
    """Decorador que mede o tempo de execução de uma função"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"⏱️  {func.__name__} executou em {execution_time:.4f} segundos")
        return result
    return wrapper


# Decorador para cache com TTL (Time To Live)
def cache_with_ttl(ttl_seconds: int = 300):
    """Decorador que implementa cache com expiração"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Criar chave única para os argumentos
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            # Verificar se existe no cache e não expirou
            if key in cache:
                cached_time, cached_result = cache[key]
                if current_time - cached_time < ttl_seconds:
                    print(f"🎯 Cache hit para {func.__name__}")
                    return cached_result
            
            # Executar função e armazenar no cache
            result = func(*args, **kwargs)
            cache[key] = (current_time, result)
            print(f"💾 Resultado armazenado no cache para {func.__name__}")
            return result
        
        return wrapper
    return decorator


# Context manager personalizado
@contextmanager
def performance_monitor(operation_name: str):
    """Context manager para monitorar performance de operações"""
    print(f"🚀 Iniciando operação: {operation_name}")
    start_time = time.time()
    start_memory = 0  # Simulado - em produção usaria psutil
    
    try:
        yield
    except Exception as e:
        print(f"❌ Erro durante {operation_name}: {e}")
        raise
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"✅ {operation_name} concluída em {duration:.4f}s")


# Classe abstrata demonstrando ABC
class DataProcessor(ABC):
    """Classe abstrata para processadores de dados"""
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Método abstrato para processar dados"""
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Método abstrato para validar dados"""
        pass


# Implementação concreta usando dataclass
@dataclass
class PythonDataProcessor(DataProcessor):
    """Processador de dados específico para Python"""
    name: str
    version: str
    features: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Método executado após inicialização do dataclass"""
        if not self.features:
            self.features = ["POO", "Funcional", "Imperativa"]
    
    def process(self, data: Any) -> Dict[str, Any]:
        """Processa dados aplicando características do Python"""
        with performance_monitor(f"Processamento de dados - {self.name}"):
            # Usar list comprehension (característica do Python)
            processed_features = [f.upper() for f in self.features if len(f) > 2]
            
            # Usar dict comprehension
            feature_lengths = {feature: len(feature) for feature in self.features}
            
            return {
                "processor": self.name,
                "version": self.version,
                "processed_features": processed_features,
                "feature_lengths": feature_lengths,
                "original_data": data
            }
    
    def validate(self, data: Any) -> bool:
        """Valida dados de entrada"""
        return data is not None and len(str(data)) > 0


# Metaclass personalizada (recurso avançado)
class SingletonMeta(type):
    """Metaclass que implementa o padrão Singleton"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Classe usando metaclass
class ConfigurationManager(metaclass=SingletonMeta):
    """Gerenciador de configuração usando padrão Singleton"""
    
    def __init__(self):
        self.config = {
            "app_name": "Python & JavaScript Presentation",
            "version": "1.0.0",
            "debug": True,
            "features": ["decorators", "context_managers", "metaclasses"]
        }
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Define valor de configuração"""
        self.config[key] = value


# Função com type hints avançados
def process_multiple_data_types(
    data: Union[str, int, List[str], Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Função que demonstra type hints avançados e processamento de múltiplos tipos
    """
    if isinstance(data, str):
        return {"type": "string", "length": len(data), "upper": data.upper()}
    elif isinstance(data, int):
        return {"type": "integer", "value": data, "squared": data ** 2}
    elif isinstance(data, list):
        return {
            "type": "list", 
            "length": len(data), 
            "items": [item.upper() if isinstance(item, str) else item for item in data]
        }
    elif isinstance(data, dict):
        return {"type": "dict", "keys": list(data.keys()), "size": len(data)}
    else:
        return None


# Função usando programação funcional
@measure_time
@cache_with_ttl(ttl_seconds=60)
def functional_data_analysis(numbers: List[int]) -> Dict[str, Any]:
    """
    Análise de dados usando programação funcional
    """
    # Usar filter, map e reduce (functools.reduce)
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    squared_numbers = list(map(lambda x: x ** 2, numbers))
    
    # Usar functools.reduce para somar todos os números
    total_sum = functools.reduce(lambda a, b: a + b, numbers, 0)
    
    # List comprehension com condição
    positive_squares = [x ** 2 for x in numbers if x > 0]
    
    return {
        "original": numbers,
        "even_numbers": even_numbers,
        "squared_numbers": squared_numbers,
        "total_sum": total_sum,
        "positive_squares": positive_squares,
        "statistics": {
            "count": len(numbers),
            "max": max(numbers) if numbers else 0,
            "min": min(numbers) if numbers else 0,
            "avg": total_sum / len(numbers) if numbers else 0
        }
    }


# Property e setter (encapsulamento)
class PythonFeatureDemo:
    """Classe demonstrando properties e encapsulamento"""
    
    def __init__(self, name: str):
        self._name = name
        self._features = []
        self._score = 0
    
    @property
    def name(self) -> str:
        """Getter para nome"""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Setter para nome com validação"""
        if not isinstance(value, str) or len(value) < 2:
            raise ValueError("Nome deve ser uma string com pelo menos 2 caracteres")
        self._name = value
    
    @property
    def score(self) -> int:
        """Score calculado baseado no número de features"""
        return len(self._features) * 10
    
    def add_feature(self, feature: str) -> None:
        """Adiciona uma feature"""
        if feature not in self._features:
            self._features.append(feature)
    
    def get_features(self) -> List[str]:
        """Retorna cópia das features (encapsulamento)"""
        return self._features.copy()
    
    def __str__(self) -> str:
        """Representação string"""
        return f"PythonFeatureDemo(name='{self.name}', features={len(self._features)}, score={self.score})"
    
    def __repr__(self) -> str:
        """Representação técnica"""
        return f"PythonFeatureDemo(name='{self.name}', features={self._features})"


# Função principal para demonstrar todas as características
def demonstrate_python_features():
    """Função que demonstra todas as características avançadas do Python"""
    print("🐍 Demonstração de Características Avançadas do Python\n")
    
    # 1. Singleton
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    print(f"Singleton test: {config1 is config2}")  # True
    
    # 2. Dataclass e processamento
    processor = PythonDataProcessor(
        name="Advanced Python Processor",
        version="3.11",
        features=["Decorators", "Context Managers", "Metaclasses", "Type Hints"]
    )
    
    # 3. Context manager
    with performance_monitor("Processamento de dados complexos"):
        result = processor.process("Dados de exemplo")
        print(f"Resultado do processamento: {result}")
    
    # 4. Programação funcional com decoradores
    numbers = [1, 2, 3, 4, 5, -1, -2, 0, 10, 15]
    analysis = functional_data_analysis(numbers)
    print(f"Análise funcional: {analysis}")
    
    # 5. Properties e encapsulamento
    demo = PythonFeatureDemo("Python Demo")
    demo.add_feature("Legibilidade")
    demo.add_feature("Simplicidade")
    demo.add_feature("Versatilidade")
    print(f"Demo object: {demo}")
    
    # 6. Type hints avançados
    test_data = ["Python", "JavaScript"]
    result = process_multiple_data_types(test_data)
    print(f"Processamento de tipos múltiplos: {result}")
    
    print("\n✅ Demonstração concluída!")


if __name__ == "__main__":
    demonstrate_python_features()

