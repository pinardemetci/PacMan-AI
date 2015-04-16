# WELCOME TO PACMAN - AI!
SofDes Spring'15 final project by Kelly Brennan, Stephanie Northway, and Pinar Demetci.
The project aims to use AI and machine learning strategies for pathfinding in PacMan. 

In this page:
- Project Proposal
- Design Review Preparation
- Design Review Reflection

# Project Proposal:

- Big Idea:  We aim to implement computer learning to strategize and win Pacman game. We’ll be exploring AI concepts to develop game strategies.
- MVP: Plays pacman without the ghosts and implements pathfinding and a simple AI strategy to consume food in the shortest amount of time
- Stretched goals: Plays pacman well with ghosts. Implement a neural network

## Learning Goals:
- Kelly - Getting more experience with object oriented programming; data processing; learn about machine learning; think about other applications of machine learning; gain more confidence coding and experience debugging; working with github efficiently 
- Pinar - Learning about AI, machine learning and algorithms, practicing object-oriented programming, collaborative coding and using GitHub effectively.
- Steph - Learning AI concepts, being a decent team member on a software project, writing good tests and documentation
- Shared - Learning AI concepts, being good collaborators and teammates

## Implementation Plan: 
Identified a library or framework that you think will be useful for you project. If you don’t have any idea how you will implement your project, provide a rough plan for how you will determine this information


The framework laid out in Berkeley’s CS188 class (http://ai.berkeley.edu/project_overview.html) will provide us with sufficient scaffolding, including an implementation of the Pacman game in Python, to get started. There may even be a bit too much scaffolding in the course materials; we will discuss as a team how much of it we want to make use of. We will likely use the numpy and scipy libraries for the machine learning part of the project.

## Project Schedule: 

### Week 1: 
- Start the Machine Learning and AI and Algorithms toolbox
- Set up Github, install numpy/scipy
- Go through the Berkely CS188 site to see what is available, decide what to use (Individual)

### Week 2:  
- Start the skeleton of the website.
- First stab at architecture
- Keeping track of Pacman location and begin AI in finding food
- Design Review

### Week 3: 
- Have MVP
- Code Review
- UML diagram
- Decide which advanced learning strategy we want to use
- Work on website

### Week 4: 
- Working on advanced learning strategy
- Continue website development

### Week 5:
- “Mid”-Project Presentation (4/23)
- Continue website development

### Week 6: 
- Finishing touches on code and website
- Final poster and demo session (Wednesday, May 6th from 4pm - 7pm)

### Collaboration Plan:
- Have formal weekly meetings Sundays 3-5pm and informal meetings on Wednesdays 9pm-12am when we can
- Work on implementing specific parts of program between meetings
- Pair programming during weekly meetings
- Software development strategies
- Pair programming during meetings
- Good Git practices: feature branches and pull requests

### Risks: 
- AI/machine learning is hard! It may be a little much for us to implement a successful AI in 6 weeks. Also, relying on Berkeley’s code and having to go through and understand it could be a bottleneck. Leaving the website development into the end. Senioritis.

### Additional Course Content: 
- Covering more AI and machine learning related concepts -additional to the toolboxes- would be useful. 
- Coding/data processing efficiency 

#Code Review I: Preparation and Framing
##**Background and Context**: 
* Project goal: Develop our own artificial intelligence algorithm for the pacman agent to learn how to play based on the agent’s experience in earning rewards by acting on different states
  *  Continuing to use the UC Berkeley code as the foundation of our AI algorithm
* We have abstracted the game by focusing on agent collecting food and not including ghosts (... for now…)
* Plan to implement Q learning adaptation that uses a linear combination of the agent’s set of states and actions
* * Instead of using a Q matrix, as a we presented last time, because the number of states to keep track of in a game would be infeasible
* * Please see Reinforcement Learning: Q Learning Adaptation handout for high level overview
* We are currently considering using the python library called python to implement the learning algorithm
* * We will contact Gabrielle, who has previous experience using pybrain, to learn more about the library and how to use it

# Design Review I: Preparation and Framing

## What we want to get out the design review:
- Clarify how we are going to encode the states because there are many complicated variables associated with pacman. Ex. Ghosts, capsules, bonus capsule. 
- Identify next steps

## Background and Context:
Project structure uses existing code from a computer science class at UC Berkeley. We are developing our own artificial intelligence algorithm to learn how to play pacman. The code we write will control the agent in the game to ultimately win as it learns from it’s experience. 
Please look the introduction and Q-learning questions on: http://ai.berkeley.edu/reinforcement.html 
Q-learning tutorial: ttp://mnemstudio.org/path-finding-q-learning-tutorial.htm
This tutorial was used to develop our first basic q-learning example

## Key Questions: 
- Best way to encode states? Especially with regard to ghosts
- Distance from closest ghost?
- Separate encoding for every ghost, since they behave differently?
- What happens when they are scared? Do we need a whole other R matrix?
- To what extent, if any, should we modify the Berkeley game structure code to improve our project?

## Agenda for Technical Review Session: (25 minutes)
- 5 min introducing the project + existing game architecture
- 10 min on encoding problem
- explain our current approach: show paper and draw it out on white board. 
- ask other teams if they see any issues with this or have better ways to do it
- 10 min on code architecture
- discuss our current state of affairs
- collaboratively ideate on what would be most effective
- should we mess with the Berkeley code?
- Identify next steps

## Feedback:
Pygame Neural Fitted Q learning. Has features to add such as pellets around you, ghosts around you etc. board size doesn’t really matter I guess?

### Reflection and Synthesis
# Review Process Reflection

## How did the Review go?
Our design review was very helpful because we addressed our key questions that helped us re-oriented our project direction in the future to use more feasible solutions in learning and keeping track of pacman’s states and actions. Considering how much we learned from the design review, we used our time effectively and efficiently. In the design review, we showed how we have implemented Q-learning into our code and how we are working with the Berkeley code structure. Showing the audience demonstrations of our current process helped them better understand our current challenges and provide constructive, helpful feedback. Overall, the design review quite successful because the feedback helped us think critically about our process and progress and helped reorient us in a more feasible direction in terms of storing pacman states and actions and developing the AI algorithm.

## Did we get answers to our key questions?

- Question 1
To what extent, if any, should we modify the Berkeley game structure code to improve our project?

- Answer 1
Based on the design review, we determined to focus our energy on getting the artificial intelligence function for a functional pacman (our MVP). We will modify the code only as necessary to obtain that goal. 

- Question 2
Best way to encode states? Especially with regard to ghosts (distance from closest ghost? Separate encoding for ever ghost, since they behave differently? What happens when they are scared? Do we need a whole other R matrix?)

- Answer 2
Our audience suggested that we have a Q function instead of a Q matrix because, with our current plan, the number of pacman states would be so large that enumeration would take a very long time. The Q function would feature a vector input of pacman’s states and give a weighted output. This sounds like a much better, more efficient option.  

In order to learn, pacman must share knowledge across very similar states. The states and action must be stored in some what (TBD - see below). The R matrix could be a function a specific state. For example it would include whether pacman ate a capsule.

 In teams of implementing AI, we have been thinking about pacman’s actions at the single step level and we like the suggestion to think more about pacman’s actions at a high level. This would involve building pacman’s actions as block strategies (“Go towards the pellet in the upper lefthand corner”. “Go away from ghost”). For example, one of the strategies may involve using astar for pacman to find a path to the desired location.The block strategy would be continuously updated in pacman’s long-term plan.

Since we are using pacman code from a Berkeley CS class, a student pointed out that it will be important for us to consider how the students in the Berkeley CS class address the same problem. While we want to be careful about not “cheating”, we think this may be a good idea to answer some of our high-level questions. 

To address this question, we received good recommendations for resources to use in developing our code. Specifically, using pybrain, a modular Machine Learning Library for python the includes powerful algorithms for learning tasks, and/or Neurogammon Tesauro, that includes neural network layers. 

We hope to implement and test our all of these suggestions because they have helped us recognize the constraints of our current direction. We will become more familiar with the different resources and test them as we continue our progress. 

### Did we stick closely to our planned agenda, or did we consider new things during the discussion that made you change your plans?
    
For the most part, we stuck closely to the planned agenda. We spent about two minutes introducing the project. Then we launched into explaining Q-learning in order to explain our problem of encoding pacman’s states and actions more efficiently. We received extensive feedback about using a Q-function and implementing block strategies that was very helpful. While we spent a significant amount of time (~15 minutes), going over Q-learning, introducing our challenge, and receiving feedback, the time was well spent because it helped us reevaluate our current direction and modify it quite extensively but using functions instead of matrices. 
We introduced the current game architecture with a UML diagram and how we interact with it. Then, we showed demonstrations of the simple algorithms we had developed, a Q-learning example and a simple-exploration (based specifically on explored and unexplored cells). We asked to what extent we should modify the Berkeley code structure and determines that our next steps were to focus on pacman’s AI algorithm. 

### What could you do next time to have an even more effective technical review?

Distributed “sparknote” sheets of the concepts, such as Q-learning, that we want to talk about. We recognize that Q-learning is a difficult concept to understand just through reading a website. This would allow our audience to have a document to refer to as we discuss how we have incorporated the concepts into our code and, if desired, take notes. 
Do more back of the envelope calculations of project functions before hand to get a better sense of the limitations of our current project direction.

## Feedback and Decisions:

### How do you plan to incorporate feedback going forward?

Going forward, we will develop the Q function and vector input. Additionally, we will test storing pacman’s learned states with various methods (including pickling). In our learning function, we will use some of the suggested resources to help our code be more efficient. Instead of focusing on pacman’s single actions, we will construct and test the high-level block strategies. Then, integrate them into various states. With learning, pacman will begin to choose the optimal block strategies based on it’s current state. Through this process, we may refer more to the Berkeley code as we encounter significant challenges to obtain an overview of our other students address the same problem.

### What new questions did we generate?

- How to use pybrain and incorporate into our code structure? (Currently working on this)
- How to use astar in moving pacman, not just identifying a path? (Currently working on this)
- How to convert text into a matrix with pickling? (Currently working on this) Are there better options to consider in storing knowledge between similar states?
- What weighted variables are important to include in the weighted vector of pacman’s state? (Pacman’s priorities?) Precisely, how should we weight them?
- How to store pacman’s similar states and actions for learning process? Set of vectors?
