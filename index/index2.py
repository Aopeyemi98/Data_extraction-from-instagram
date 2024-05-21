import instaloader
import csv

def extract_instagram_data(username, num_posts, num_comments):
    # Create an instance of the Instaloader class
    loader = instaloader.Instaloader()

    # Load the profile from the username

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile '{username}' does not exist.")
        return
    except instaloader.exceptions.ConnectionException:
        print("Failed to connect to Instagram.")
        return

    # Create a CSV file to store the data
    with open(f'{username}_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter="|")

        # Write the header row
        writer.writerow(['Post ID', 'Post URL', 'Post Caption', 'Comment_ID', 'Comment_Username', 'Comment_Text', 'Comment_Likes'])

        # Iterate over the posts
        for post in profile.get_posts():
            # Get the post ID, URL and CAPTION
            post_id = post.mediaid
            post_url = f"https://www.instagram.com/p/{post.shortcode}/"
            post_caption = post.caption

            # Get the comments
            comments = []
            comment_count = 0
            for comment in post.get_comments():
                if comment_count >= num_comments:
                    break
                comments.append([{
                    'comment_id': comment.id["Comment_id"],
                    'comment_owner': comment.owner.username,
                    'comment_text': comment.text,
                    'comment_likes': comment.likes_count,
                    }])
            comment_count += 1


            # Write the post data to the CSV file
            writer.writerow([post_id, post_url, post_caption] + comments[:num_comments])

            # Stop after num_posts posts
            if num_posts <= 0:
                break
            num_posts -= 1

    print(f"Data saved to {username}_data.csv")
    

# Example usage
extract_instagram_data('adenuga.ope', 1, 1)