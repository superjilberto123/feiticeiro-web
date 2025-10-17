import React, { useState, useEffect, useRef } from 'react';
import { Sword, Sparkles, Heart, Droplet, Shield } from 'lucide-react';

const FFBattleSystem = () => {
  const [vidaJogador, setVidaJogador] = useState(150);
  const [manaJogador, setManaJogador] = useState(100);
  const [vidaInimigo, setVidaInimigo] = useState(180);
  const [manaInimigo, setManaInimigo] = useState(80);
  
  const [pocoesVida, setPocoesVida] = useState(3);
  const [pocoesMana, setPocoesMana] = useState(2);
  const [elixirs, setElixirs] = useState(1);
  
  const [turnoJogador, setTurnoJogador] = useState(true);
  const [animacaoAtiva, setAnimacaoAtiva] = useState(false);
  const [mensagens, setMensagens] = useState([
    '⚔️ Uma nova batalha épica começou!',
    '👹 O Demônio das Sombras emerge das trevas!',
    '🗡️ Escolha sua ação sabiamente...'
  ]);
  
  const [menuAtivo, setMenuAtivo] = useState(null);
  const [gameOver, setGameOver] = useState(false);
  const [vitoria, setVitoria] = useState(false);
  
  const [guerreiroEstado, setGuerreiroEstado] = useState('idle');
  const [demonioEstado, setDemonioEstado] = useState('idle');
  
  const maxVidaJogador = 150;
  const maxManaJogador = 100;
  const maxVidaInimigo = 180;
  
  const adicionarMensagem = (msg) => {
    setMensagens(prev => [...prev.slice(-5), msg]);
  };
  
  const executarAtaqueFisico = (tipo) => {
    if (!turnoJogador || animacaoAtiva) return;
    
    setAnimacaoAtiva(true);
    setMenuAtivo(null);
    
    const ataques = {
      1: { nome: 'Corte Rápido', dano: 25, precisao: 85 },
      2: { nome: 'Golpe Trovão', dano: 35, precisao: 70 },
      3: { nome: 'Tornado Cortante', dano: 45, precisao: 60 },
      4: { nome: 'Impacto Sísmico', dano: 55, precisao: 50 }
    };
    
    const ataque = ataques[tipo];
    adicionarMensagem(`🗡️ ${ataque.nome}!`);
    
    setGuerreiroEstado('attack');
    
    setTimeout(() => {
      const chance = Math.random() * 100;
      if (chance <= ataque.precisao) {
        const dano = Math.floor(Math.random() * (ataque.dano * 0.2) + ataque.dano * 0.8);
        setVidaInimigo(prev => Math.max(0, prev - dano));
        setDemonioEstado('hurt');
        adicionarMensagem(`💥 Acertou! ${dano} de dano!`);
        
        setTimeout(() => setDemonioEstado('idle'), 400);
      } else {
        adicionarMensagem('💨 Errou!');
      }
      
      setGuerreiroEstado('idle');
      setTimeout(verificarFimTurno, 1000);
    }, 600);
  };
  
  const executarMagia = (tipo) => {
    if (!turnoJogador || animacaoAtiva) return;
    
    const magias = {
      1: { nome: 'Fire III', dano: 40, precisao: 80, custo: 15 },
      2: { nome: 'Blizzard III', dano: 38, precisao: 85, custo: 18 },
      3: { nome: 'Thunder III', dano: 42, precisao: 75, custo: 20 },
      4: { nome: 'Holy', dano: 50, precisao: 90, custo: 25 },
      5: { nome: 'Meteor', dano: 70, precisao: 60, custo: 35 }
    };
    
    const magia = magias[tipo];
    
    if (manaJogador < magia.custo) {
      adicionarMensagem('❌ MP insuficiente!');
      return;
    }
    
    setAnimacaoAtiva(true);
    setMenuAtivo(null);
    setManaJogador(prev => prev - magia.custo);
    
    adicionarMensagem(`🔮 ${magia.nome}!`);
    
    setTimeout(() => {
      const chance = Math.random() * 100;
      if (chance <= magia.precisao) {
        const dano = Math.floor(Math.random() * (magia.dano * 0.2) + magia.dano * 0.8);
        setVidaInimigo(prev => Math.max(0, prev - dano));
        setDemonioEstado('hurt');
        adicionarMensagem(`✨ Acertou! ${dano} de dano!`);
        
        setTimeout(() => setDemonioEstado('idle'), 600);
      } else {
        adicionarMensagem('💨 A magia falhou!');
      }
      
      setTimeout(verificarFimTurno, 1500);
    }, 800);
  };
  
  const usarPocaoVida = () => {
    if (pocoesVida <= 0 || !turnoJogador) return;
    
    setPocoesVida(prev => prev - 1);
    const cura = Math.floor(Math.random() * 20 + 40);
    setVidaJogador(prev => Math.min(prev + cura, maxVidaJogador));
    
    adicionarMensagem(`❤️ Poção usada! Recuperou ${cura} HP!`);
    setMenuAtivo(null);
    
    setTimeout(verificarFimTurno, 800);
  };
  
  const usarPocaoMana = () => {
    if (pocoesMana <= 0 || !turnoJogador) return;
    
    setPocoesMana(prev => prev - 1);
    const recuperacao = Math.floor(Math.random() * 20 + 30);
    setManaJogador(prev => Math.min(prev + recuperacao, maxManaJogador));
    
    adicionarMensagem(`💙 Éter usado! Recuperou ${recuperacao} MP!`);
    setMenuAtivo(null);
    
    setTimeout(verificarFimTurno, 800);
  };
  
  const usarElixir = () => {
    if (elixirs <= 0 || !turnoJogador) return;
    
    setElixirs(prev => prev - 1);
    setVidaJogador(maxVidaJogador);
    setManaJogador(maxManaJogador);
    
    adicionarMensagem('✨ Elixir usado! HP e MP restaurados!');
    setMenuAtivo(null);
    
    setTimeout(verificarFimTurno, 1000);
  };
  
  const defender = () => {
    if (!turnoJogador || animacaoAtiva) return;
    
    setMenuAtivo(null);
    adicionarMensagem('🛡️ Você se prepara para defender!');
    setManaJogador(prev => Math.min(prev + 10, maxManaJogador));
    
    setTimeout(verificarFimTurno, 800);
  };
  
  const verificarFimTurno = () => {
    setAnimacaoAtiva(false);
    
    if (vidaInimigo <= 0) {
      fimDeJogo(true);
    } else {
      setTimeout(turnoInimigo, 500);
    }
  };
  
  const turnoInimigo = () => {
    setTurnoJogador(false);
    setAnimacaoAtiva(true);
    
    const acao = Math.random() * 100;
    
    setTimeout(() => {
      if (acao <= 60) {
        // Ataque físico
        const dano = Math.floor(Math.random() * 15 + 25);
        setVidaJogador(prev => Math.max(0, prev - dano));
        setDemonioEstado('attack');
        adicionarMensagem(`👹 Garra Sombria! ${dano} de dano!`);
        setGuerreiroEstado('hurt');
        
        setTimeout(() => {
          setDemonioEstado('idle');
          setGuerreiroEstado('idle');
        }, 600);
      } else if (acao <= 85) {
        // Magia
        if (manaInimigo >= 15) {
          const dano = Math.floor(Math.random() * 15 + 30);
          setManaInimigo(prev => prev - 15);
          setVidaJogador(prev => Math.max(0, prev - dano));
          adicionarMensagem(`👹 Bola de Fogo Negra! ${dano} de dano mágico!`);
          setGuerreiroEstado('hurt');
          
          setTimeout(() => setGuerreiroEstado('idle'), 600);
        }
      } else {
        // Curar
        const cura = Math.floor(Math.random() * 15 + 25);
        setVidaInimigo(prev => Math.min(prev + cura, maxVidaInimigo));
        adicionarMensagem(`🩸 Inimigo recuperou ${cura} HP!`);
      }
      
      setTimeout(fimTurnoInimigo, 1200);
    }, 800);
  };
  
  const fimTurnoInimigo = () => {
    if (vidaJogador <= 0) {
      fimDeJogo(false);
    } else {
      setTurnoJogador(true);
      setAnimacaoAtiva(false);
    }
  };
  
  const fimDeJogo = (isVitoria) => {
    setGameOver(true);
    setVitoria(isVitoria);
    setAnimacaoAtiva(true);
    
    if (isVitoria) {
      adicionarMensagem('🎉 VITÓRIA! O Demônio foi derrotado!');
      adicionarMensagem('✨ Você ganhou 500 EXP e 200 Gil!');
      setDemonioEstado('dead');
    } else {
      adicionarMensagem('💀 DERROTA! Você foi derrotado...');
      adicionarMensagem('🔄 Tente novamente!');
      setGuerreiroEstado('dead');
    }
  };
  
  const reiniciar = () => {
    setVidaJogador(150);
    setManaJogador(100);
    setVidaInimigo(180);
    setManaInimigo(80);
    setPocoesVida(3);
    setPocoesMana(2);
    setElixirs(1);
    setTurnoJogador(true);
    setAnimacaoAtiva(false);
    setGameOver(false);
    setMenuAtivo(null);
    setGuerreiroEstado('idle');
    setDemonioEstado('idle');
    setMensagens([
      '⚔️ Uma nova batalha épica começou!',
      '👹 O Demônio das Sombras emerge das trevas!',
      '🗡️ Escolha sua ação sabiamente...'
    ]);
  };
  
  const BarraProgresso = ({ valor, max, cor }) => (
    <div className="w-full bg-gray-800 h-6 rounded-lg overflow-hidden border-2 border-gray-600">
      <div 
        className={`h-full transition-all duration-500 ${cor}`}
        style={{ width: `${(valor / max) * 100}%` }}
      />
    </div>
  );
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-950 via-purple-950 to-black text-white p-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-6 text-yellow-400 tracking-wider">
          ⚔️ FINAL FANTASY BATTLE ARENA ⚔️
        </h1>
        
        {/* Campo de Batalha */}
        <div className="bg-gradient-to-b from-blue-900 to-purple-900 rounded-lg p-8 mb-6 border-4 border-blue-500 min-h-[300px] relative overflow-hidden">
          {/* Estrelas de fundo */}
          <div className="absolute inset-0">
            {[...Array(30)].map((_, i) => (
              <div 
                key={i}
                className="absolute w-1 h-1 bg-white rounded-full"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 60}%`,
                  opacity: Math.random() * 0.8 + 0.2
                }}
              />
            ))}
          </div>
          
          <div className="flex justify-between items-center relative z-10">
            {/* Guerreiro */}
            <div className={`text-center transition-all ${guerreiroEstado === 'attack' ? 'translate-x-20' : ''} ${guerreiroEstado === 'hurt' ? 'animate-pulse' : ''}`}>
              <div className="text-8xl mb-2">🗡️</div>
              <div className="font-bold text-yellow-300">GUERREIRO</div>
            </div>
            
            {/* VS */}
            <div className="text-6xl font-bold text-red-500 animate-pulse">VS</div>
            
            {/* Demônio */}
            <div className={`text-center transition-all ${demonioEstado === 'attack' ? '-translate-x-20' : ''} ${demonioEstado === 'hurt' ? 'animate-pulse' : ''} ${demonioEstado === 'dead' ? 'opacity-30' : ''}`}>
              <div className="text-8xl mb-2">👹</div>
              <div className="font-bold text-red-400">DEMÔNIO</div>
            </div>
          </div>
        </div>
        
        {/* Status */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Jogador */}
          <div className="bg-blue-900 p-4 rounded-lg border-2 border-yellow-500">
            <h3 className="text-xl font-bold text-yellow-400 mb-3">🗡️ GUERREIRO MÍSTICO</h3>
            <div className="space-y-2">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-red-400 font-bold">HP</span>
                  <span>{vidaJogador}/{maxVidaJogador}</span>
                </div>
                <BarraProgresso valor={vidaJogador} max={maxVidaJogador} cor="bg-red-600" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-blue-400 font-bold">MP</span>
                  <span>{manaJogador}/{maxManaJogador}</span>
                </div>
                <BarraProgresso valor={manaJogador} max={maxManaJogador} cor="bg-blue-600" />
              </div>
            </div>
          </div>
          
          {/* Inimigo */}
          <div className="bg-purple-900 p-4 rounded-lg border-2 border-red-500">
            <h3 className="text-xl font-bold text-red-400 mb-3">👹 DEMÔNIO DAS SOMBRAS</h3>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-red-400 font-bold">HP</span>
                <span>{vidaInimigo}/{maxVidaInimigo}</span>
              </div>
              <BarraProgresso valor={vidaInimigo} max={maxVidaInimigo} cor="bg-purple-600" />
            </div>
          </div>
        </div>
        
        {/* Mensagens */}
        <div className="bg-blue-950 p-4 rounded-lg border-2 border-blue-600 mb-6 min-h-[120px]">
          {mensagens.map((msg, idx) => (
            <div key={idx} className="text-sm mb-1 font-mono">{msg}</div>
          ))}
        </div>
        
        {/* Menu de Ações */}
        {!gameOver && (
          <div className="bg-blue-900 p-6 rounded-lg border-2 border-blue-500">
            {!menuAtivo ? (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button
                  onClick={() => setMenuAtivo('ataque')}
                  disabled={!turnoJogador || animacaoAtiva}
                  className="bg-red-600 hover:bg-red-700 disabled:bg-gray-600 p-4 rounded-lg font-bold text-lg transition-all"
                >
                  ⚔️ ATACAR
                </button>
                <button
                  onClick={() => setMenuAtivo('magia')}
                  disabled={!turnoJogador || animacaoAtiva}
                  className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 p-4 rounded-lg font-bold text-lg transition-all"
                >
                  🔮 MAGIA
                </button>
                <button
                  onClick={() => setMenuAtivo('itens')}
                  disabled={!turnoJogador || animacaoAtiva}
                  className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 p-4 rounded-lg font-bold text-lg transition-all"
                >
                  💊 ITENS
                </button>
                <button
                  onClick={defender}
                  disabled={!turnoJogador || animacaoAtiva}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 p-4 rounded-lg font-bold text-lg transition-all"
                >
                  🛡️ DEFENDER
                </button>
              </div>
            ) : (
              <div>
                <button 
                  onClick={() => setMenuAtivo(null)}
                  className="mb-4 bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded"
                >
                  ← Voltar
                </button>
                
                {menuAtivo === 'ataque' && (
                  <div className="grid grid-cols-2 gap-3">
                    <button onClick={() => executarAtaqueFisico(1)} className="bg-red-700 hover:bg-red-800 p-3 rounded">
                      🗡️ Corte Rápido
                    </button>
                    <button onClick={() => executarAtaqueFisico(2)} className="bg-red-700 hover:bg-red-800 p-3 rounded">
                      ⚡ Golpe Trovão
                    </button>
                    <button onClick={() => executarAtaqueFisico(3)} className="bg-red-700 hover:bg-red-800 p-3 rounded">
                      🌪️ Tornado Cortante
                    </button>
                    <button onClick={() => executarAtaqueFisico(4)} className="bg-red-700 hover:bg-red-800 p-3 rounded">
                      💥 Impacto Sísmico
                    </button>
                  </div>
                )}
                
                {menuAtivo === 'magia' && (
                  <div className="grid grid-cols-2 gap-3">
                    <button onClick={() => executarMagia(1)} className="bg-purple-700 hover:bg-purple-800 p-3 rounded">
                      🔥 Fire III (15 MP)
                    </button>
                    <button onClick={() => executarMagia(2)} className="bg-purple-700 hover:bg-purple-800 p-3 rounded">
                      ❄️ Blizzard III (18 MP)
                    </button>
                    <button onClick={() => executarMagia(3)} className="bg-purple-700 hover:bg-purple-800 p-3 rounded">
                      ⚡ Thunder III (20 MP)
                    </button>
                    <button onClick={() => executarMagia(4)} className="bg-purple-700 hover:bg-purple-800 p-3 rounded">
                      🌟 Holy (25 MP)
                    </button>
                    <button onClick={() => executarMagia(5)} className="bg-purple-700 hover:bg-purple-800 p-3 rounded col-span-2">
                      🌪️ Meteor (35 MP)
                    </button>
                  </div>
                )}
                
                {menuAtivo === 'itens' && (
                  <div className="space-y-3">
                    <button 
                      onClick={usarPocaoVida} 
                      disabled={pocoesVida <= 0}
                      className="w-full bg-green-700 hover:bg-green-800 disabled:bg-gray-600 p-3 rounded"
                    >
                      ❤️ Poção Vida x{pocoesVida}
                    </button>
                    <button 
                      onClick={usarPocaoMana}
                      disabled={pocoesMana <= 0}
                      className="w-full bg-green-700 hover:bg-green-800 disabled:bg-gray-600 p-3 rounded"
                    >
                      💙 Éter x{pocoesMana}
                    </button>
                    <button 
                      onClick={usarElixir}
                      disabled={elixirs <= 0}
                      className="w-full bg-green-700 hover:bg-green-800 disabled:bg-gray-600 p-3 rounded"
                    >
                      ✨ Elixir x{elixirs}
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
        
        {/* Tela de Game Over */}
        {gameOver && (
          <div className="text-center">
            <div className={`text-6xl font-bold mb-6 ${vitoria ? 'text-yellow-400' : 'text-red-500'}`}>
              {vitoria ? '🎉 VITÓRIA! 🎉' : '💀 DERROTA 💀'}
            </div>
            <button 
              onClick={reiniciar}
              className="bg-yellow-600 hover:bg-yellow-700 px-8 py-4 rounded-lg font-bold text-xl"
            >
              🔄 NOVA BATALHA
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default FFBattleSystem;
