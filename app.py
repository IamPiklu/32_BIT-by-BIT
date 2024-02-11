from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from final import (
    handwriting_to_text,
    guide_to_txt,
    compare,
)  # replace 'your_module' with the name of your module

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        # get the uploaded files
        pdf_file = request.files["pdf"]
        guide_file = request.files["guide"]

        # save the files
        pdf_path = secure_filename(pdf_file.filename)
        guide_path = secure_filename(guide_file.filename)
        pdf_file.save(pdf_path)
        guide_file.save(guide_path)

        # process the files
        answers_text = handwriting_to_text(pdf_path)
        guide_text = guide_to_txt(guide_path)

        prompt = (
            "below is the teachers guide\n\n"
            + guide_text
            + "\n\n\n\n\nbelow is the transcription of a students answer script \n\n"
            + answers_text
            + "\n\n\n\n\nI want you to evaluate the students answer script based on teacher's guide. Teachers guide contains the bare minimum points or keywords that the teacher is looking for in the answer.\nRules for evaluation:-\n1)ignore spelling and grammar mistake\n2)marking allotted for each answers is mentioned in teachers guide\n3)give full marks if all the points from the teachers guide are present in the students answers\n4)if points are missing then give marks accordingly or partially\nreturn the total marks obtained by the student at the last"
        )
        review = compare(prompt)

        return {"review": review}

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
