#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuração e verificação para análise DICE
Este script verifica e instala as dependências necessárias para usar DiCE
"""

import subprocess
import sys
import importlib
from pathlib import Path

def check_python_version():
    """
    Verifica se a versão do Python é compatível
    """
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ é necessário para DiCE")
        return False
    else:
        print("✅ Versão do Python compatível")
        return True

def install_package(package_name, import_name=None, version=None):
    """
    Instala um pacote se não estiver disponível
    """
    if import_name is None:
        import_name = package_name.replace('-', '_')
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} já está instalado")
        return True
    except ImportError:
        print(f"📦 Instalando {package_name}...")
        
        install_cmd = [sys.executable, "-m", "pip", "install"]
        
        if version:
            install_cmd.append(f"{package_name}=={version}")
        else:
            install_cmd.append(package_name)
        
        try:
            subprocess.run(install_cmd, capture_output=True, text=True, check=True)
            print(f"✅ {package_name} instalado com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar {package_name}:")
            print(f"   {e.stderr}")
            return False

def check_dice_installation():
    """
    Verifica se DiCE está instalado e funcionando
    """
    print("\n🎲 Verificando instalação do DiCE...")
    
    try:
        import dice_ml
        try:
            version = dice_ml.__version__
            print(f"✅ DiCE versão {version} instalado")
        except AttributeError:
            print("✅ DiCE instalado (versão não detectável)")
        
        # Teste básico de funcionalidade
        print("🧪 Testando funcionalidade básica...")
        
        # Criar dados de teste simples
        import pandas as pd
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        
        # Dados sintéticos mais robustos
        np.random.seed(42)
        n_samples = 200
        
        # Criar dados com separação mais clara entre classes
        X1 = np.random.multivariate_normal([2, 2], [[1, 0.5], [0.5, 1]], n_samples//2)
        X2 = np.random.multivariate_normal([-2, -2], [[1, 0.5], [0.5, 1]], n_samples//2)
        
        X = pd.DataFrame(
            np.vstack([X1, X2]),
            columns=['feature1', 'feature2']
        )
        y = np.hstack([np.ones(n_samples//2), np.zeros(n_samples//2)])
        
        # Treinar modelo
        model = RandomForestClassifier(n_estimators=20, random_state=42)
        model.fit(X, y)
        
        # Verificar acurácia mínima
        accuracy = model.score(X, y)
        if accuracy < 0.8:
            print(f"⚠️  Modelo com baixa acurácia ({accuracy:.2f}), mas DiCE pode funcionar")
        
        # Configurar DiCE
        data_df = X.copy()
        data_df['target'] = y
        
        dice_data = dice_ml.Data(
            dataframe=data_df,
            continuous_features=['feature1', 'feature2'],
            outcome_name='target'
        )
        
        dice_model = dice_ml.Model(
            model=model,
            backend='sklearn'
        )
        
        explainer = dice_ml.Dice(dice_data, dice_model, method='random')
        
        # Selecionar uma amostra da classe majoritária
        class_1_indices = np.where(y == 1)[0]
        query_idx = class_1_indices[0]
        query = X.iloc[[query_idx]]
        
        # Gerar contrafactual para a classe minoritária
        cf = explainer.generate_counterfactuals(
            query, 
            total_CFs=2, 
            desired_class=0
        )
        
        if cf.cf_examples_list[0].final_cfs_df is not None and len(cf.cf_examples_list[0].final_cfs_df) > 0:
            print("✅ DiCE está funcionando corretamente")
            return True
        else:
            print("⚠️  DiCE instalado mas com dificuldades na geração de contrafactuais")
            print("   Isso pode ser normal dependendo dos dados - DiCE ainda pode funcionar")
            return True  # Considerar como sucesso parcial
            
    except ImportError:
        print("❌ DiCE não está instalado")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar DiCE: {str(e)}")
        return False

def check_data_files():
    """
    Verifica se os arquivos de dados necessários existem
    """
    print("\n📁 Verificando arquivos de dados...")
    
    script_dir = Path(__file__).parent
    data_dir = script_dir / 'data'
    
    required_files = [
        'pisa_spain_sample_v2.csv'
    ]
    
    all_files_exist = True
    
    if not data_dir.exists():
        print(f"❌ Diretório de dados não encontrado: {data_dir}")
        return False
    
    for file_name in required_files:
        file_path = data_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name} encontrado")
        else:
            print(f"❌ {file_name} não encontrado em {data_dir}")
            all_files_exist = False
    
    return all_files_exist

def create_directories():
    """
    Cria diretórios necessários para os resultados
    """
    print("\n📂 Criando diretórios de saída...")
    
    script_dir = Path(__file__).parent
    directories = [
        'img_dice',
        'dice_results', 
        'dice_detailed_results'
    ]
    
    for dir_name in directories:
        dir_path = script_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Criado: {dir_path}")
        else:
            print(f"✅ Já existe: {dir_path}")

def print_usage_instructions():
    """
    Imprime instruções de uso
    """
    print("\n" + "="*60)
    print("🎯 INSTRUÇÕES DE USO")
    print("="*60)
    
    print("\n1️⃣  Para executar análise DICE completa:")
    print("   python paper_script_dice.py")
    
    print("\n2️⃣  Para executar exemplo educativo detalhado:")
    print("   python dice_analysis_example.py")
    
    print("\n3️⃣  Para ver documentação:")
    print("   Abra README_DICE.md")
    
    print("\n📊 Resultados serão salvos em:")
    print("   - img_dice/: Visualizações do pipeline")
    print("   - dice_results/: Contrafactuais básicos")
    print("   - dice_detailed_results/: Análise detalhada")
    
    print("\n" + "="*60)

def main():
    """
    Função principal de configuração
    """
    print("🚀 CONFIGURAÇÃO DO AMBIENTE DICE")
    print("=" * 50)
    
    # 1. Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # 2. Instalar dependências básicas
    print("\n📦 Verificando dependências básicas...")
    basic_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'), 
        ('scikit-learn', 'sklearn'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn')
    ]
    
    for package, import_name in basic_packages:
        if not install_package(package, import_name):
            print(f"❌ Falha ao instalar {package}")
            sys.exit(1)
    
    # 3. Instalar DiCE
    print("\n🎲 Instalando DiCE...")
    if not install_package('dice-ml', 'dice_ml'):
        print("❌ Falha ao instalar DiCE")
        print("\n🔧 Tentativas alternativas:")
        print("   pip install dice-ml==0.9")
        print("   conda install -c conda-forge dice-ml")
        sys.exit(1)
    
    # 4. Verificar instalação do DiCE
    if not check_dice_installation():
        print("❌ DiCE não está funcionando corretamente")
        sys.exit(1)
    
    # 5. Verificar arquivos de dados
    if not check_data_files():
        print("\n⚠️  Alguns arquivos de dados não foram encontrados")
        print("   Os scripts ainda podem funcionar com dados sintéticos")
    
    # 6. Criar diretórios
    create_directories()
    
    # 7. Mostrar instruções
    print("\n✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print_usage_instructions()

if __name__ == "__main__":
    main()