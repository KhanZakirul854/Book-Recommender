from flask import Flask, render_template, request
import pickle
import numpy as np


selected_books_dataset=pickle.load(open('selected.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(selected_books_dataset['Book-Title'].values),
                           author = list(selected_books_dataset['Book-Author'].values),
                           image = list(selected_books_dataset['Image-URL-M'].values),
                           votes = list(selected_books_dataset['num-ratings'].values),
                           ratings = list(selected_books_dataset['avg-ratings'].values),)


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]

    # Get similar items
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[
                    1:6]  # calculated the similarity score & store them

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)
        #str(user_input) #issue- had to convert it to a string

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process form submission here
        pass  # Placeholder for processing form submission
    else:
        # Render the contact form
        return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True)
