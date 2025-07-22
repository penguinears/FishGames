from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Paste your full games_in_order list here (the one you shared above)

def simulate_game(players):
    total_players = len(players)
    prize_per_player = 1_000_000
    total_prize = total_players * prize_per_player

    log = []
    log.append(f"{total_players} players entered. Final prize: ${total_prize:,}\n")

    for game in games_in_order:
        if len(players) < game["min_players"]:
            log.append(f"Not enough players for {game['name']} (need {game['min_players']}). Skipping.\n")
            continue

        log.append(f"\n🎮 {game['name']}\n{game['phase']}\n")

        if len(players) == 1:
            log.append(f"Only one player remains: {players[0]} — automatic winner!")
            break

        if game["name"] == "Tug of War":
            random.shuffle(players)
            half = len(players) // 2
            team1 = players[:half]
            team2 = players[half:]
            losing_team = random.choice([team1, team2])
            survivors = [p for p in players if p not in losing_team]
            eliminated = losing_team

        elif game["name"] == "Marbles":
            random.shuffle(players)
            survivors = []
            eliminated = []
            for i in range(0, len(players)-1, 2):
                winner = random.choice([players[i], players[i+1]])
                loser = players[i+1] if winner == players[i] else players[i]
                survivors.append(winner)
                eliminated.append(loser)
            if len(players) % 2 == 1:
                survivors.append(players[-1])

        elif game["name"] == "Squid Game (Final Game)":
            eliminated = random.sample(players, len(players) - 1)
            survivors = [p for p in players if p not in eliminated]

        else:
            elim_count = max(1, len(players) // 2)
            eliminated = random.sample(players, elim_count)
            survivors = [p for p in players if p not in eliminated]

        for e in eliminated:
            msg = random.choice(game['elimination_msgs'])
            log.append(f"💀 {e} {msg}")

        log.append(f"\n✅ Survivors remaining: {len(survivors)}\n")
        players = survivors

        if len(players) == 0:
            log.append("☠️ Everyone is eliminated. No one wins the money!")
            return "\n".join(log)

    if len(players) == 1:
        winner = players[0]
        log.append(f"\n🏆 {winner} is the SOLE WINNER of The Fish Games!")
        log.append(f"Prize Won: ${total_prize:,}")
    else:
        log.append("Multiple players survived, but only one can win. Something went wrong!")

    return "\n".join(log)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        raw_players = request.form.get("players")
        if not raw_players:
            return render_template("index.html", error="Please enter at least 2 players.")
        players = [p.strip() for p in raw_players.split(",") if p.strip()]
        if len(players) < 2:
            return render_template("index.html", error="Please enter at least 2 players.")
        result_log = simulate_game(players)
        return render_template("result.html", log=result_log.replace("\n", "<br>"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
