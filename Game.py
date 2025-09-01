from browser import document, timer
import random

# --- state ---
wins = 0
losses = 0
ties = 0

choices = {
    "rock": "✊ Rock",
    "paper": "✋ Paper",
    "scissors": "✌️ Scissors"
}

# --- helper functions ---
def update_score():
    document["score"].text = "Wins: " + str(wins) + " | Losses: " + str(losses) + " | Ties: " + str(ties)

def show_result(txt):
    el = document["result"]
    el.text = txt
    el.classList.add("show", "pulse")
    # remove pulse quickly so it can run again next time
    def _clear():
        el.classList.remove("pulse")
    timer.set_timeout(_clear, 600)

def _highlight(node_id, ms=800):
    node = document[node_id]
    node.classList.add("winner-glow")
    def _rm():
        node.classList.remove("winner-glow")
    timer.set_timeout(_rm, ms)

def animate_effect(winner):
    el = document["result"]
    # remove old classes
    el.classList.remove("scissors-slash", "rock-smash", "paper-wrap")
    
    if winner == "scissors":
        el.classList.add("scissors-slash")
    elif winner == "rock":
        el.classList.add("rock-smash")
    elif winner == "paper":
        el.classList.add("paper-wrap")
    
    # remove animation class after it ends so it can trigger again
    def clear():
        el.classList.remove("scissors-slash", "rock-smash", "paper-wrap")
    timer.set_timeout(clear, 800)

def play(ev):
    global wins, losses, ties
    user = ev.target.id
    cpu = random.choice(list(choices.keys()))

    if user == cpu:
        ties += 1
        show_result("🤝 Tie — both chose " + choices[user])
    elif (user == "rock" and cpu == "scissors") or \
         (user == "paper" and cpu == "rock") or \
         (user == "scissors" and cpu == "paper"):
        wins += 1
        show_result("🎉 You win! " + choices[user] + " beats " + choices[cpu])
        _highlight(user)
        animate_effect(user)
    else:
        losses += 1
        show_result("💻 Computer wins! " + choices[cpu] + " beats " + choices[user])
        _highlight(cpu)
        animate_effect(cpu)

    update_score()

def reset_score(ev):
    global wins, losses, ties
    wins = losses = ties = 0
    update_score()
    show_result("🔄 Score reset — good luck!")

# --- bind events ---
for key in choices.keys():
    document[key].bind("click", play)

document["reset"].bind("click", reset_score)

# --- initial ---
update_score()
