<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contextual Bandit Benchmarks</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 60px 40px;
            max-width: 900px;
            width: 100%;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            background-size: 300% 300%;
            animation: gradientShift 3s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .main-title {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
            line-height: 1.1;
            animation: fadeInUp 0.8s ease-out;
        }
        
        .subtitle {
            font-size: 1.5rem;
            color: #6b7280;
            font-weight: 500;
            margin-bottom: 40px;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }
        
        .authors {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 12px;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }
        
        .author {
            font-size: 1.1rem;
            font-weight: 600;
            color: #374151;
            padding: 8px 16px;
            background: rgba(103, 126, 234, 0.1);
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        
        .author:hover {
            background: rgba(103, 126, 234, 0.2);
            transform: translateY(-2px);
        }
        
        .institution {
            font-size: 1rem;
            color: #9ca3af;
            font-weight: 400;
            margin-bottom: 50px;
            animation: fadeInUp 0.8s ease-out 0.6s both;
        }
        
        .divider {
            width: 100px;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 0 auto 40px;
            animation: fadeInUp 0.8s ease-out 0.8s both;
        }
        
        .project-section {
            background: rgba(103, 126, 234, 0.05);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 30px;
            border: 1px solid rgba(103, 126, 234, 0.1);
            animation: fadeInUp 0.8s ease-out 1s both;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #374151;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .project-description {
            font-size: 1.1rem;
            color: #6b7280;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .highlight {
            font-weight: 600;
            color: #667eea;
        }
        
        .dataset-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            padding: 12px 24px;
            background: rgba(103, 126, 234, 0.1);
            border-radius: 12px;
            transition: all 0.3s ease;
            border: 1px solid rgba(103, 126, 234, 0.2);
        }
        
        .dataset-link:hover {
            background: rgba(103, 126, 234, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px -8px rgba(103, 126, 234, 0.3);
        }
        
        .icon {
            width: 20px;
            height: 20px;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .floating-elements {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }
        
        .floating-element {
            position: absolute;
            background: rgba(103, 126, 234, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        .floating-element:nth-child(1) {
            width: 60px;
            height: 60px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .floating-element:nth-child(2) {
            width: 40px;
            height: 40px;
            top: 70%;
            right: 15%;
            animation-delay: 2s;
        }
        
        .floating-element:nth-child(3) {
            width: 80px;
            height: 80px;
            bottom: 20%;
            left: 5%;
            animation-delay: 4s;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 40px 24px;
                margin: 20px;
            }
            
            .main-title {
                font-size: 2.5rem;
            }
            
            .subtitle {
                font-size: 1.2rem;
            }
            
            .authors {
                flex-direction: column;
                gap: 12px;
            }
            
            .project-section {
                padding: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="floating-elements">
            <div class="floating-element"></div>
            <div class="floating-element"></div>
            <div class="floating-element"></div>
        </div>
        
        <h1 class="main-title">Contextual Bandit Benchmarks</h1>
        <h2 class="subtitle">Final Project - Reinforcement Learning</h2>
        
        <div class="authors">
            <span class="author">Oliver Tausendschoen</span>
            <span class="author">Marvin Ernst</span>
            <span class="author">Timothy Cassel</span>
        </div>
        
        <p class="institution">Barcelona School of Economics • 2025</p>
        
        <div class="divider"></div>
        
        <div class="project-section">
            <h3 class="section-title">
                <svg class="icon" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Project Overview
            </h3>
            <p class="project-description">
                This project focuses on comparing <span class="highlight">classical contextual bandits</span> 
                to <span class="highlight">neural contextual bandits</span>, exploring the effectiveness 
                of modern deep learning approaches versus traditional methods in multi-armed bandit scenarios.
            </p>
            <a href="https://github.com/st-tech/zr-obp" class="dataset-link" target="_blank">
                <svg class="icon" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"/>
                </svg>
                Open Bandit Pipeline Dataset
            </a>
        </div>
    </div>
</body>
</html>