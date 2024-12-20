from flask import Flask, request, render_template_string
import portalocker

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        content = request.form['content']
        with open('file.txt', 'a') as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                file.write(content + '\n')
                portalocker.unlock(file)
                message = "Content written to file."
            except portalocker.LockException:
                message = "Unable to lock file."

    return render_template_string('''
    <form method="post">
        <textarea name="content" rows="4" cols="50"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    <p>{{ message }}</p>
    ''', message=message)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
