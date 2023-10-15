# Discord Role Expire

A Discord bot to give a role to a member for a specified amount of time, and automatically remove it.

## Deployment

Bot is deployed to AWS [Lightsail](https://lightsail.aws.amazon.com/ls/webapp/us-west-2/instances/Discord_Expire_Roles_Bot_1/connect) and being ran using the `nohup` command.

Learn more here: [nohup](https://www.geeksforgeeks.org/nohup-command-in-linux-with-examples/#)

PID of process is saved to `pid.txt`
Output of process is in `out.log`

To start process, run:
```
nohup make start > out.log 2>&1 &
echo $1 > pid.txt
```

To kill process, run:
```
kill -9 `cat pid.txt`
rm pid.txt
```

Learn more here: [Stackoverflow](https://stackoverflow.com/questions/17385794/how-to-get-the-process-id-to-kill-a-nohup-process)