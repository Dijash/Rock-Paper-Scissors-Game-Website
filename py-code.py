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
    def _clear():
        el.classList.remove("pulse")
    timer.set_timeout(_clear, 700)

def _highlight(node_id, ms=800):
    node = document[node_id]
    node.classList.add("winner-glow")
    def _rm():
        node.classList.remove("winner-glow")
    timer.set_timeout(_rm, ms)

def animate_button(node_id):
    node = document[node_id]
    node.classList.remove("scissors-slash", "rock-smash", "paper-wrap")
    if node_id == "scissors":
        node.classList.add("scissors-slash")
    elif node_id == "rock":
        node.classList.add("rock-smash")
    elif node_id == "paper":
        node.classList.add("paper-wrap")
    def clear():
        node.classList.remove("scissors-slash", "rock-smash", "paper-wrap")
    timer.set_timeout(clear, 800)

def tie_animation():
    for key in choices.keys():
        document[key].classList.add("tie-shake")
    def clear():
        for key in choices.keys():
            document[key].classList.remove("tie-shake")
    timer.set_timeout(clear, 600)

# --- main game logic ---
def play(ev):
    global wins, losses, ties
    user = ev.target.id
    cpu = random.choice(list(choices.keys()))

    if user == cpu:
        ties += 1
        show_result("🤝 Tie — both chose " + choices[user])
        tie_animation()
    elif (user == "rock" and cpu == "scissors") or \
         (user == "paper" and cpu == "rock") or \
         (user == "scissors" and cpu == "paper"):
        wins += 1
        show_result("🎉 You win! " + choices[user] + " beats " + choices[cpu])
        _highlight(user)
        animate_button(user)
    else:
        losses += 1
        show_result("💻 Computer wins! " + choices[cpu] + " beats " + choices[user])
        _highlight(cpu)
        animate_button(cpu)

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
# --- IGNORE ---
