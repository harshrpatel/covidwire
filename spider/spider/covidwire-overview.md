# CovidWire Tech Briefing
### By Kevin Zeidler, Senior Developer
### 29 June, 2020

This document is intended to provide a high-level outline of the CovidWire tech stack suitable for a general audience.  Accordingly, technical details of various components and custom machine learning models that together comprise will be simplified as much as possible. At a high level, the CovidWire backend is not a single piece of software, but a pipeline of 'transformer' layers working in concert. Each layer constitutes a small, discrete part of a machine with an ambitious goal: to connect users with actionable, high-quality updates on the global COVID-19 pandemic, as witnessed through the eyes of their own neighbors and communities. Because nowhere is the tragedy and scope of a mass viral contagion event more apparent than in our cities: from overcrowded hospitals, to agonizing local debates over the reopening of schools, restaurants, parks, and places of worship -- and increasingly, now, whether to reclose them. 

By necessity, CovidWire crawls thousands of news articles every day in order to achieve this goal. But merely aggregating the news doesn't get you very far without the ability to distinguish between relevant and irrelevant articles,  because -- as the news cycle has gyrated back and forth between topics including the pandemic, the election, and civil unrest -- COVID-19 stories constitute only a small fraction of global news. But even that, as it turns out, isn't enough, because 'relevance' is in the eye of the beholder. For example, when a governor orders all bars and restaurants in her state to shut down until further notice, the consequences are far-reaching and reverberate everywhere within the borders of that state. When a mayor, on the other hand, orders all bars and restaurants in her city to do the same, the consequences for city residents are practically the same. But outside the borders of that city, not so much. The two actions, superfically similar though they may be, differ profoundly in terms of the scope of their effects. The question, in other words, isn't simply whether a particular story is COVID-relevant, or even where it takes place, but *_to whom_* it is relevant. Or more simply, where should it be shown? Machines ordinarily struggle to answer questions like this. What makes CovidWire unique is our use of neural network-based classifiers to efficiently predict an "best guess" answer to this question with a high degree of accuracy.  

  how to articles are relevant, but to identify specific regional audiences to whom those articles become relevant. At the same time, we must ensure that we *_never_* feature content that contradicts the advice of public health officials.

   identify specific regional audiences to whom those article is most relevant    These capabilities is enabled in part by state-of-the-art NLP (natural language processing) models to extract meaningful references to locations from an article's text and infer the specific regional audience to whom those articles are most relevant. The final output of the 

## Machine Learning

