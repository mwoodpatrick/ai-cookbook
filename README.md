# Introduction

This Cookbook contains examples and tutorials to help developers build AI systems, offering copy/paste code snippets that you can easily integrate into your own projects.

## Setup environment

You should first create and activate a virtual environment:

```sh
$ nix-shell
$ python -m venv venv/ # create virtual environment
$ source venv/bin/activate # activate virtual environment
$ pip install --upgrade pip # ensure we are using latest pip
$ pip install -r requirements.txt # install requirements
```

Install the pinned dependencies from `requirements.txt`:

```sh
(venv) $ python -m pip install -r requirements.txt
```

Then you can execute the provided Python scripts, for example:

```sh
(venv) $ python basic_logging.py
```

## Rendering Docs

To convert the README.md to html use:

```sh
pandoc README.md -o README.html
```

To display the generated html file use:

```sh
firefox README.html &
```


## About Me

Hi! I'm Dave, AI Engineer and founder of Datalumina®. On my [YouTube channel](https://www.youtube.com/@daveebbelaar?sub_confirmation=1), I share practical tutorials that teach developers how to build AI systems that actually work in the real world. Beyond these tutorials, I also help people start successful freelancing careers. Check out the links below to learn more!

### Explore More Resources

Whether you're a learner, a freelancer, or a business looking for AI expertise, we've got something for you:

1. **Learning Python for AI and Data Science?**  
   Join our **free community, Data Alchemy**, where you'll find resources, tutorials, and support  
   ▶︎ [Learn Python for AI](https://www.skool.com/data-alchemy)

2. **Ready to start or scale your freelancing career?**  
   Learn how to land clients and grow your business  
   ▶︎ [Find freelance projects](https://www.datalumina.com/data-freelancer)

3. **Need expert help on your next project?**  
   Work with me and my team to solve your data and AI challenges  
   ▶︎ [Work with me](https://www.datalumina.com/solutions)

4. **Already building AI applications?**  
   Explore the **GenAI Launchpad**, our production framework for AI systems  
   ▶︎ [Explore the GenAI Launchpad](https://launchpad.datalumina.com/)
