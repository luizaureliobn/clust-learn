#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline Completo de Análise de Clusters PISA

Este script automatiza a execução completa do processo de análise:
1. Executa o script principal (paper_script.py) para gerar visualizações
2. Extrai informações detalhadas dos clusters (extract_cluster_info.py)
3. Gera relatório completo (generate_cluster_report.py)

Autor: Sistema de Análise PISA
Data: 2024
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_separator(title):
    """Imprime um separador visual com título"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def run_script(script_path, description):
    """Executa um script Python e captura sua saída"""
    print(f"🚀 Iniciando: {description}")
    print(f"📄 Script: {script_path}")
    print(f"⏰ Horário: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)
    
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script não encontrado: {script_path}")
        
        # Executar o script
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(script_path)
        )
        end_time = time.time()
        
        # Calcular tempo de execução
        execution_time = end_time - start_time
        
        # Verificar se houve erro
        if result.returncode != 0:
            print(f"❌ ERRO na execução de {description}")
            print(f"Código de saída: {result.returncode}")
            print(f"Erro: {result.stderr}")
            return False
        
        # Sucesso
        print(f"✅ CONCLUÍDO: {description}")
        print(f"⏱️  Tempo de execução: {execution_time:.2f} segundos")
        
        # Mostrar saída se houver
        if result.stdout.strip():
            print("\n📋 Saída do script:")
            print("-" * 30)
            print(result.stdout)
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao executar {description}: {str(e)}")
        return False

def main():
    """Função principal do pipeline"""
    print_separator("PIPELINE COMPLETO DE ANÁLISE DE CLUSTERS PISA")
    
    print(f"📅 Data/Hora de início: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    print(f"📁 Diretório de trabalho: {os.getcwd()}")
    
    # Definir caminhos dos scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    scripts = [
        {
            'path': os.path.join(script_dir, 'paper_script.py'),
            'description': 'Análise Principal e Geração de Visualizações',
            'details': 'Executa pré-processamento, redução de dimensionalidade, clustering e classificação'
        },
        {
            'path': os.path.join(script_dir, 'extract_cluster_info.py'),
            'description': 'Extração de Informações dos Clusters',
            'details': 'Extrai estatísticas detalhadas e características dos clusters identificados'
        },
        {
            'path': os.path.join(script_dir, 'generate_cluster_report.py'),
            'description': 'Geração de Relatório Completo',
            'details': 'Cria relatório detalhado com análise e interpretação dos resultados'
        }
    ]
    
    # Verificar se todos os scripts existem
    print("🔍 Verificando disponibilidade dos scripts...")
    missing_scripts = []
    for script in scripts:
        if not os.path.exists(script['path']):
            missing_scripts.append(script['path'])
            print(f"❌ Script não encontrado: {script['path']}")
        else:
            print(f"✅ Script encontrado: {os.path.basename(script['path'])}")
    
    if missing_scripts:
        print(f"\n❌ ERRO: {len(missing_scripts)} script(s) não encontrado(s). Pipeline abortado.")
        return False
    
    print("\n✅ Todos os scripts estão disponíveis. Iniciando execução...")
    
    # Executar scripts em sequência
    total_start_time = time.time()
    successful_executions = 0
    
    for i, script in enumerate(scripts, 1):
        print_separator(f"ETAPA {i}/3: {script['description'].upper()}")
        print(f"📝 Detalhes: {script['details']}")
        print()
        
        success = run_script(script['path'], script['description'])
        
        if success:
            successful_executions += 1
            print(f"\n🎉 Etapa {i} concluída com sucesso!")
        else:
            print(f"\n💥 Etapa {i} falhou!")
            
            # Perguntar se deve continuar
            response = input("\n❓ Deseja continuar com as próximas etapas? (s/n): ").lower().strip()
            if response not in ['s', 'sim', 'y', 'yes']:
                print("\n🛑 Pipeline interrompido pelo usuário.")
                break
        
        # Pausa entre scripts (exceto no último)
        if i < len(scripts):
            print("\n⏳ Aguardando 2 segundos antes da próxima etapa...")
            time.sleep(2)
    
    # Resumo final
    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    
    print_separator("RESUMO FINAL DO PIPELINE")
    print(f"📊 Scripts executados com sucesso: {successful_executions}/{len(scripts)}")
    print(f"⏱️  Tempo total de execução: {total_execution_time:.2f} segundos")
    print(f"📅 Finalizado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    
    if successful_executions == len(scripts):
        print("\n🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
        print("\n📁 Arquivos gerados:")
        print("   • Visualizações na pasta 'img/'")
        print("   • Relatório de clusters (arquivo .txt com timestamp)")
        print("   • Informações detalhadas dos clusters (saída no console)")
        return True
    else:
        print(f"\n⚠️  PIPELINE PARCIALMENTE CONCLUÍDO ({successful_executions}/{len(scripts)} etapas)")
        return False

def show_help():
    """Mostra informações de ajuda"""
    print("\n" + "=" * 60)
    print(" PIPELINE COMPLETO DE ANÁLISE DE CLUSTERS PISA ".center(60, "="))
    print("=" * 60)
    print("\nEste pipeline automatiza a execução completa da análise:")
    print("\n1. 📊 paper_script.py")
    print("   - Executa análise principal com visualizações")
    print("   - Gera gráficos na pasta 'img/'")
    print("\n2. 🔍 extract_cluster_info.py")
    print("   - Extrai informações detalhadas dos clusters")
    print("   - Mostra estatísticas no console")
    print("\n3. 📝 generate_cluster_report.py")
    print("   - Gera relatório completo em arquivo .txt")
    print("   - Inclui análise e interpretação dos resultados")
    print("\nUso:")
    print("   python pipeline_completo.py        # Executa pipeline completo")
    print("   python pipeline_completo.py --help # Mostra esta ajuda")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
    else:
        try:
            success = main()
            sys.exit(0 if success else 1)
        except KeyboardInterrupt:
            print("\n\n🛑 Pipeline interrompido pelo usuário (Ctrl+C)")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n💥 ERRO CRÍTICO no pipeline: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)