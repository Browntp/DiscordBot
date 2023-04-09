import discord
import response
import sqlite3

conn = sqlite3.connect("bot.db")
c = conn.cursor()
#c.execute("""CREATE TABLE users(
    #user_number integer PRIMARY KEY,
    #stage integer,
    #exp integer,
    #speed_stat real,
    #attack_stat real,
    #health_stat real,
    #max_stat integer,
    #stat_points real
    #)""")




#c.execute("""CREATE TABLE minimum(
   #user_number integer PRIMARY KEY,
    #min_meditation integer,
    #min_journaling integer,
    #min_exercise integer,
    #min_coldshower integer,
    #amnt_meditation integer,
    #amnt_journaling integer,
    #amnt_exercise integer,
    #amnt_coldshower integer,
    #min_reading integer,
    #amnt_reading integer,
    #min_morningroutine integer,
    #amnt_morningroutine integer,
    #min_nightroutine integer,
    #amnt_nightroutine integer,
    #min_work integer,
    #amnt_work integer,
    #min_challengesfaced integer,
    #amnt_challengesfaced integer
   #)""")


#challenge: set a value to true until you level up to three once your about to level up to four return "You have a challenge,"
#after you complete the challenge then set the value to true and level up.



embed_color = discord.Colour.dark_teal()
embed_title = "Title"
embed_description = "Description"

embed = discord.Embed(
    colour=embed_color,
    description=embed_description,
    title=embed_title
)


async def database(message, message_user):
    message2 = message_user.lower()
    message3 = message2[1:]
    message4 = message3.split(" ")
    if(message4[0] == "tstart"):
         c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (message.author.id, 1, 0, 1, 1, 1, 50, 0))
         c.execute("INSERT INTO minimum VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.author.id, 20, 2, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
         embed.description = "Database initialized."
         role_name = "Stage 1"
         role = discord.utils.get(message.guild.roles, name=role_name)
         if role:
             await message.author.add_roles(role)

         conn.commit()
         return embed

    elif(message4[0] == "tstatscheck"):
        c.execute("SELECT  stage, exp, speed_stat, attack_stat, health_stat, max_stat, stat_points FROM users WHERE user_number = ?", (message.author.id,))
        result = c.fetchone()
        c.execute("SELECT * FROM minimum WHERE user_number = ?", (message.author.id,))
        result2 = c.fetchone()
        if result:
            stats_statement = f"""
                Stage: {result[0]}
               speed: {result[2]}
               attack: {result[3]}
               health: {result[4]}
               MaxPossible: {result[5]}
               Stat Points Available: {result[6]} 
               -TASKS REQUIRED FOR BREAKTHROUGH- 
                exp: {result[1]}/{result[0] * 100 * result[0]}
                {f"Meditation Minutes: {result2[5]}/{result2[1]}" if result2[1] != 0  else "" }
                {f"Exercise Minutes: {result2[7]}/{result2[3]}" if result2[2] != 0  else "" }
                {f"Journaling entries: {result2[6]}/{result2[2]}" if result2[3] != 0  else "" }
                {f"Reading Minutes: {result2[10]}/{result2[9]}" if result2[9] != 0  else "" }
                {f"Cold Shower Minutes: {result2[8]}/{result2[4]}" if result2[4] != 0  else "" }
                {f"Daily Morning Routine: {result2[12]}/{result2[11]}" if result2[11] != 0  else "" }
                {f"Daily Night Routine: {result2[14]}/{result2[13]}" if result2[13] != 0  else "" }
                {f"Work minutes: {result2[16]}/{result2[15]}" if result2[15] != 0  else "" }
                {f"Hated challenges: {result2[18]}/{result2[17]}" if result2[17] != 0  else "" }
                """

            embed.description = stats_statement
            embed.title = "Stats description"
            return embed

        else:
            embed.description = "no stats"
            return embed
    elif message4[0] == "tcheckobject":
        if (message.author.id == 690664788338016267):
            c.execute("SELECT * FROM users")
            result = c.fetchall()
            c.execute("SELECT * FROM minimum")
            result2 = c.fetchall()
            if result:
                statement = f"""
                            Table users: {str(result)}
                            Table minimum: {str(result2)}
                                """
                embed.description = statement
                return embed
            else:
                embed.description = "Database is empty."
                return embed
        else:
            embed.description = "You do not have sufficient authority"
            return embed


    elif(message4[0] == "tdelete"):
        c.execute("DELETE FROM users WHERE user_number = ?", (message.author.id,))
        c.execute("DELETE FROM minimum WHERE user_number = ?", (message.author.id,))
        embed.description = "Your data has been deleted."
        embed.title = "Delete Data"
        member = message.author
        for x in range(9):
            role_name = f"Stage {x + 1}"
            role = discord.utils.get(message.guild.roles, name=role_name)
            try:
                await member.remove_roles(role)
            except:
                break
        return embed
    elif(message4[0] == "tclose"):
        if(message.author.id == 690664788338016267):
            conn.close()
            embed.description = "Database has been closed"
            return embed
        else:
            embed.description = "You do not have the sufficient authority"
            return embed





async def input_tasks(message, message_user):
    c.execute("SELECT * FROM users WHERE user_number = ?", (message.author.id,))
    result = c.fetchone()
    embed.title = "Stat Points"
    message2 = message_user.lower()
    message3 = message2[1:]
    message4 = message3.split(" ")
    amount_spending = float(message4[2])
    if result[7] - amount_spending < 0:
        embed.description = """You do not have enough SP
                               Do some tasks in order to gain SP
                               type: !tasks 
                            """
        return embed

    if message4[0] == "increasestat":
        if len(message4) != 3:
            embed.description = """
                            Invalid command. Please specify a valid stat to increase and the amount to increase it by:
                            !increasestat speed x
                            !increasestat attack x
                            !increasestat health x
                            """
            return embed



        if result:

            if message4[1] == "speed":
                new_stat = result[3] + amount_spending
                if new_stat > result[6]:
                    embed.description = "Cannot increase stat beyond max possible."
                    return embed
                else:
                    c.execute("UPDATE users SET speed_stat = ?, stat_points = ? WHERE user_number = ?",
                              (new_stat, result[7] - amount_spending, message.author.id))
                    conn.commit()
                    embed.description = f"speed stat increased to {new_stat}!"
                    return embed

            elif message4[1] == "attack":
                new_stat = result[4] + amount_spending
                if new_stat > result[6]:
                    embed.description = "Cannot increase stat beyond max possible."
                    return embed
                else:
                    c.execute("UPDATE users SET attack_stat = ?, stat_points = ? WHERE user_number = ?",
                              (new_stat,result[7] - amount_spending, message.author.id))
                    conn.commit()
                    embed.description = f"attack stat increased to {new_stat}!"
                    return embed

            elif message4[1] == "health":
                new_stat = result[5] + amount_spending
                if new_stat > result[6]:
                    embed.description = "Cannot increase stat beyond max possible."
                    return embed
                else:
                    c.execute("UPDATE users SET health_stat = ?, stat_points = ? WHERE user_number = ?",
                              (new_stat, result[7] - amount_spending, message.author.id))
                    conn.commit()
                    embed.description = f"health stat increased to {new_stat}!"
                    return embed


            else:
                embed.description = """
                Invalid command. Please specify a valid stat to increase:
                speed
                attack
                health
                """
                return embed

    else:
        return "You have not started your cultivation journey yet! Use the command !tstart to begin."

async def tasks_manager(message, message_user):
    embed.title = "Daily Log"
    message2 = message_user.lower()
    message3 = message2[1:]
    message4 = message3.split(" ")
    c.execute("SELECT stage, exp, stat_points, speed_stat, attack_stat, health_stat, max_stat, stat_points FROM users WHERE user_number = ?", (message.author.id,))
    result = c.fetchone()
    c.execute("SELECT * FROM minimum")
    minimum_result = c.fetchone()
    if len(message4) != 2:
        embed.description = "Invalid command. Please specify the amount of time exercised."
        return embed
    try:
        exp = int(message4[1])
    except:
        embed.description = "Invalid command. Please specify the amount of time exercised as an integer."
        return embed
    if exp < 1:
        embed.description = "Invalid command. Please specify a positive integer value for time exercised."
        return embed

    new_exp = result[1] + exp


    if message4[0] == "logmeditation" :
        x = result[4] + (exp/5 * 0.5) if result[4] + (exp/5 * 0.5) < result[6] else result[6]
        y = result[3] + (exp/5 * 0.5) if result[3] + (exp/5 * 0.5) < result[6] else result[6]
        c.execute("UPDATE users SET exp = ?, attack_stat = ?, speed_stat = ? WHERE user_number = ?",
                  (new_exp, x, y, message.author.id))
        c.execute("UPDATE minimum SET amnt_meditation = ? WHERE user_number = ?", (minimum_result[5] + exp , message.author.id))
        conn.commit()
        embed.description = f"""
                            Exp gained: {exp}
                            Attack points gained: {exp/5 * 0.5}
                            Speed Points gained: {exp/5 * 0.5}
                            """
    elif message4[0] == "logexercise":
        x = result[5] + (exp / 5 * 0.75) if result[5] + (exp / 5 * 0.75) < result[6] else result[6]
        y = result[3] + (exp / 5 * 0.25) if result[3] + (exp / 5 * 0.25) < result[6] else result[6]
        c.execute("UPDATE users SET exp = ?, health_stat = ?, speed_stat = ? WHERE user_number = ?",
                  (new_exp,x , y, message.author.id))
        c.execute("UPDATE minimum SET amnt_exercise = ? WHERE user_number = ?", (minimum_result[7] + exp, message.author.id))
        conn.commit()
        embed.description = f"""
                                            Exp gained: {exp}
                                            Health Points gained: {exp / 5 * 0.75}
                                            Speed Points gained: {exp / 5 * 0.25}
                                            """

    elif message4[0] == "logjournaling":
        new_exp = result[1] + exp * 10
        x = result[3] + (exp * 2) if result[3] + (exp * 2) < result[6] else result[6]

        c.execute("UPDATE users SET exp = ?, speed_stat = ? WHERE user_number = ?",
                  (new_exp, x, message.author.id))
        c.execute("UPDATE minimum SET amnt_journaling = ? WHERE user_number = ?", (minimum_result[6] + exp, message.author.id))
        conn.commit()
        embed.description = f"""
                                                       Exp gained: {exp * 10}
                                                       Speed Points gained: {exp * 2}
                                                       """
    elif message4[0] == "logreading":
        if result[0] > 1:
            x = result[5] + (exp/5) if result[5] + (exp/5) < result[6] else result[6]
            c.execute("UPDATE users SET exp = ?, health_stat = ? WHERE user_number = ?",
                      (new_exp, x, message.author.id))
            c.execute("UPDATE minimum SET amnt_reading = ? WHERE user_number = ?", (minimum_result[10] + exp, message.author.id))
            conn.commit()
            embed.description = f"""
                                                           Exp gained: {exp}
                                                           Health Points gained: {exp/5}
                                                           """
        else:
            embed.description = "Your stage is not high enough for this task. The required stage is 2 for this task."

    elif message4[0] == "logcoldshower":
        if result[0] > 2:
            new_exp = result[1] + exp * 15
            x = result[5] + (exp / 5) if result[5] + (exp / 5) < result[6] else result[6]
            c.execute("UPDATE users SET exp = ?, attack_stat = ? WHERE user_number = ?",
                      (new_exp, x, message.author.id))
            c.execute("UPDATE minimum SET amnt_coldshower = ? WHERE user_number = ?", (minimum_result[8] + exp, message.author.id))
            conn.commit()
            embed.description = f"""
                                                           Exp gained: {exp * 15}
                                                           Attack Points gained: {exp * 2}
                                                           """
        else:
            embed.description = "Your stage is not high enough for this task. The required stage is 3 for this task."
    elif message4[0] == "logmorningroutine":
        if result[0] > 3:
            x = result[4] + (exp * 10) if result[4] + (exp * 10) < result[6] else result[6]
            y = result[3] + (exp * 5) if result[3] + (exp * 5) < result[6] else result[6]
            z = result[5] + (exp * 5) if result[5] + (exp * 5) < result[6] else result[6]
            new_exp = result[1] + exp * 100
            c.execute("UPDATE users SET exp = ?, attack_stat = ?, speed_stat = ?, health_stat = ? WHERE user_number = ?",
                      (new_exp, x, y, z,message.author.id))
            c.execute("UPDATE minimum SET amnt_morningroutine = ? WHERE user_number = ?", (minimum_result[12] + exp, message.author.id))
            conn.commit()
            embed.description = f"""
                                                           Exp gained: {exp * 100}
                                                           Attack Points gained: {exp * 10}
                                                           Health Points gained: {exp * 5}
                                                           Speed Points gained: {exp * 5}
                                                           """
        else:
            embed.description = "Your stage is not high enough for this task. The required stage is 4 for this task."
    elif message4[0] == "lognightroutine":
        if result[0] > 4:
            x = result[4] + (exp * 5) if result[4] + (exp * 5) < result[6] else result[6]
            y = result[3] + (exp * 5) if result[3] + (exp * 5) < result[6] else result[6]
            z = result[5] + (exp * 10) if result[5] + (exp * 10) < result[6] else result[6]
            new_exp = result[1] + exp * 100
            c.execute("UPDATE users SET exp = ?, attack_stat = ?, speed_stat = ?, health_stat = ? WHERE user_number = ?",
                      (new_exp,x , y ,z ,message.author.id))
            c.execute("UPDATE minimum SET amnt_nightroutine = ? WHERE user_number = ?", (minimum_result[14] + exp, message.author.id))
            conn.commit()
            embed.description = f"""
                                                           Exp gained: {exp * 100}
                                                           Attack Points gained: {exp * 5}
                                                           Health Points gained: {exp * 10}
                                                           Speed Points gained: {exp * 5}
                                                           """
        else:
            embed.description = "Your stage is not high enough for this task. The required stage is 5 for this task."
    elif message4[0] == "logwork":
        if result[0] > 5:
            x = result[4] + (exp/4 * 0.3) if result[4] + (exp/4 * 0.3) < result[6] else result[6]
            y = result[3] + (exp/4 * 0.7) if result[3] + (exp/4 * 0.7) < result[6] else result[6]
            c.execute("UPDATE users SET exp = ?, attack_stat = ?, speed_stat = ? WHERE user_number = ?",
                      (new_exp, x, y ,message.author.id))
            c.execute("UPDATE minimum SET amnt_work = ? WHERE user_number = ?", (minimum_result[16] + exp, message.author.id))
            conn.commit()
            embed.description = f"""
                                                           Exp gained: {exp * 1.1}
                                                           Attack Points gained: {exp/4 * 0.3}
                                                           Speed Points gained: {exp/4 * 0.7}
                                                           """
        else:
            embed.description = "Your stage is not high enough for this task. The required stage is 6 for this task."
    elif message4[0] == "logchallengesfaced":
        if result[0] > 6:
            x = result[4] + (exp * 1.5) if result[4] + (exp * 1.5) < result[6] else result[6]
            y = result[5] + (exp) if result[5] + (exp) < result[6] else result[6]
            new_exp = result[1] + exp * 10
            c.execute(
                "UPDATE users SET exp = ?, attack_stat = ?, health_stat = ? WHERE user_number = ?",
                (new_exp, x, y, message.author.id))
            c.execute("UPDATE minimum SET amnt_challengesfaced = ? WHERE user_number = ?", (minimum_result[18] + exp, message.author.id))
            conn.commit()
            embed.description = f"""
                                                               Exp gained: {exp * 10}
                                                               Attack Points gained: {exp * 1.5}
                                                               Health Points gained: {exp}
                                                               """
        else:
            embed.description = "Your stage is not high enough for this task. The required stage is 7 for this task."
    else:
        embed.description = "wrong spelling"

    c.execute("SELECT * FROM minimum")
    minimum_result = c.fetchone()
    meditation = minimum_result[5] >= minimum_result[1]
    journaling = minimum_result[6] >= minimum_result[2]
    exercise = minimum_result[7] >= minimum_result[3]
    reading = minimum_result[10] >= minimum_result[9]
    coldShower = minimum_result[8] >= minimum_result[4]
    morningRoutine = minimum_result[12] >= minimum_result[11]
    nightRoutine = minimum_result[14] >= minimum_result[13]
    work = minimum_result[16] >= minimum_result[15]
    challenges = minimum_result[18] >= minimum_result[17]
    if new_exp >= (result[0] * result[0]) * 100 and meditation and journaling and exercise and reading and coldShower and\
            morningRoutine and nightRoutine and work and challenges:
        c.execute("UPDATE users SET stage = ?, exp = ?, max_stat = ?, stat_points = ? WHERE user_number = ?",
                  (result[0] + 1, 0, result[6] * 2, result[7] + (result[0] + 1) * 10, message.author.id))
        if result[0] + 1 > 7:
            c.execute(
                "UPDATE minimum SET min_exercise = ?, min_meditation = ?, min_journaling = ?, min_reading = ?, min_coldshower = ?, min_morningroutine = ?, min_nightroutine = ?, min_work = ?, min_challengesfaced = ?, amnt_exercise = ?, amnt_meditation = ?, amnt_journaling = ?, amnt_reading = ?, amnt_coldshower = ?, amnt_morningroutine = ?, amnt_nightroutine = ?, amnt_work = ?, amnt_challengesfaced = ? WHERE user_number = ?",
                (minimum_result[3] * 2, minimum_result[1] * 2, minimum_result[2] * 2, minimum_result[9] * 2,
                 minimum_result[4] * 2, minimum_result[11] * 2, minimum_result[13] * 2, minimum_result[15] * 2, minimum_result[17] * 2, 0,
                 0,
                 0, 0, 0, 0, 0, 0, 0, minimum_result[0]))
        elif result[0] + 1 > 6:
            c.execute(
                "UPDATE minimum SET min_exercise = ?, min_meditation = ?, min_journaling = ?, min_reading = ?, min_coldshower = ?, min_morningroutine = ?, min_nightroutine = ?, min_work = ?, min_challengesfaced = ?, amnt_exercise = ?, amnt_meditation = ?, amnt_journaling = ?, amnt_reading = ?, amnt_coldshower = ?, amnt_morningroutine = ?, amnt_nightroutine = ?, amnt_work = ?, amnt_challengesfaced = ? WHERE user_number = ?",
                (minimum_result[3] * 2, minimum_result[1] * 2, minimum_result[2] * 2, minimum_result[9] * 2,
                 minimum_result[4] * 2, minimum_result[11] * 2, minimum_result[13] * 2, minimum_result[15] * 2, 10, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, minimum_result[0]))
        elif result[0] + 1 > 5:
            c.execute(
                "UPDATE minimum SET min_exercise = ?, min_meditation = ?, min_journaling = ?, min_reading = ?, min_coldshower = ?, min_morningroutine = ?, min_nightroutine = ?, min_work = ?, amnt_exercise = ?, amnt_meditation = ?, amnt_journaling = ?, amnt_reading = ?, amnt_coldshower = ?, amnt_morningroutine = ?, amnt_nightroutine = ?, amnt_work = ? WHERE user_number = ?",
                (minimum_result[3] * 2, minimum_result[1] * 2, minimum_result[2] * 2, minimum_result[9] * 2,
                 minimum_result[4] * 2, minimum_result[11] * 2, minimum_result[13] * 2, 240, 0,
                 0, 0, 0, 0, 0, 0, 0, minimum_result[0]))
        elif result[0] + 1 > 4:
            c.execute(
                "UPDATE minimum SET min_exercise = ?, min_meditation = ?, min_journaling = ?, min_reading = ?, min_coldshower = ?, min_morningroutine = ?, min_nightroutine = ?, amnt_exercise = ?, amnt_meditation = ?, amnt_journaling = ?, amnt_reading = ?, amnt_coldshower = ?, amnt_morningroutine = ?, amnt_nightroutine = ? WHERE user_number = ?",
                (minimum_result[3] * 2, minimum_result[1] * 2, minimum_result[2] * 2, minimum_result[9] * 2,
                 minimum_result[4] * 2, minimum_result[11] * 2, 5, 0,
                 0, 0, 0, 0, 0, 0, minimum_result[0]))
        elif result[0] + 1 > 3:
            c.execute(
                "UPDATE minimum SET min_exercise = ?, min_meditation = ?, min_journaling = ?, min_reading = ?, min_coldshower = ?, min_morningroutine = ?, amnt_exercise = ?, amnt_meditation = ?, amnt_journaling = ?, amnt_reading = ?, amnt_coldshower = ?, amnt_morningroutine = ? WHERE user_number = ?",
                (minimum_result[3] * 2, minimum_result[1] * 2, minimum_result[2] * 2, minimum_result[9] * 2, minimum_result[4] * 2, 5, 0, 0,
                 0, 0, 0, 0, minimum_result[0]))
        elif result[0] + 1 > 2:
            c.execute(
                "UPDATE minimum SET min_exercise = ?, min_meditation = ?, min_journaling = ?, min_reading = ?, min_coldshower = ?, amnt_exercise = ?, amnt_meditation = ?, amnt_journaling = ?, amnt_reading = ?, amnt_coldshower = ? WHERE user_number = ?",
                (minimum_result[3] * 2, minimum_result[1] * 2, minimum_result[2] * 2, minimum_result[9] * 2, 3, 0, 0, 0, 0, 0, minimum_result[0]))
        elif result[0] + 1 > 1:
            c.execute(
                "UPDATE minimum SET min_exercise = ?, min_meditation = ?, min_journaling = ?, min_reading = ?, amnt_exercise = ?, amnt_meditation = ?, amnt_journaling = ?, amnt_reading = ? WHERE user_number = ?",(
                    minimum_result[3] * 2, minimum_result[1] * 2, minimum_result[2] * 2, 30, 0, 0, 0, 0, minimum_result[0]))
        conn.commit()

        embed.description += f"""
                            CONGRATULATIONS YOU HAVE LEVELED UP TO STAGE {result[0] + 1}!
                            SP GAIN: {(result[0] + 1) * 10 }
                            MAX STAT: {result[6] * 2}
                            """
        role_name = f"Stage {result[0] + 1}"
        role = discord.utils.get(message.guild.roles, name=role_name)
        if role:
            await message.author.add_roles(role)

    return embed


async def send_message(message, user_message, isPrivate):
    try:
        if user_message[1] == "t":
            responses = await database(message, user_message)
            await message.author.send(embed=responses) if isPrivate else await message.channel.send(embed=responses)

        elif user_message[1] == "i":
            responses = await input_tasks(message, user_message)
            await message.author.send(embed=responses) if isPrivate else await message.channel.send(embed=responses)

        elif user_message[1] == "l":
            responses = await tasks_manager(message, user_message)
            await message.author.send(embed=responses) if isPrivate else await message.channel.send(embed=responses)

        else:
            responses = await response.get_response(user_message)
            await message.author.send(responses) if isPrivate else await message.channel.send(responses)

    except Exception as e:
        print(e)

def runDiscordBot():
        TOKEN = "MTA4NzA1MzIyMDg4ODcxMTIwOA.GSryXq.at2Ei0uBC0R5_XsbE5a9HoBzJ7gxqlWQVKDvT8"

        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print("I am ready")


        @client.event
        async def on_message(message):
            if message.author == client.user:
                return



            user_content = str(message.content)

            if not user_content:
                return

            if user_content[0] == "?":
                await send_message(message, user_content, True)

            elif user_content[0] == "!":

                await send_message(message, user_content, False)

            else:
                return

        client.run(TOKEN)






