Approval/ Rejection/ Status/ Active Status

@app.route('/blog_approve', methods=['POST'])
def approve_blog():
    if request.method == 'POST':
        # Get trainee_id and status from the request JSON body
        data = request.get_json()
        blog_id = data.get('blog_id')
        status = data.get('status')

        if blog_id is None or status is None:
            return jsonify({'error': "blog_id or status not provided"})

        try:
            # Convert status to string ('true' or 'false')
            status_str = 'true' if status else 'false'

            # Update trainee status in the database
            with connection.cursor() as cursor:
                cursor.execute("UPDATE blogs SET status = CASE WHEN %s = 'true' THEN 1 WHEN %s = 'false' THEN 0 ELSE status END WHERE blog_id = %s;", (status_str, status_str, int(blog_id)))
                connection.commit()
                return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': f"Database error: {str(e)}"})
    else:
        return jsonify({'error': "Only POST requests are allowed for this endpoint"})


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function updateBlogStatus(blogId, status) {
    fetch("/blog_approve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ blog_id: blogId, status: status }) // Send the status (true for approve, false for disapprove)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update button class after successful approval or disapproval
            const approveBtn = document.getElementById(`approveBTN_${blogId}`);
            approveBtn.classList.remove("btn-outline-primary");
            approveBtn.classList.add("btn-purple");
            alert("Blog status updated successfully!");
            // Reload the page after 1 second
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            alert("An error occurred: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred: " + error.message);
    });
}

</script>


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Buttons


 ${blog.status == 1 ? `<button class="btn btn-sm btn btn-purple">Selected</button>` : ''}
                        <button id="approveBTN_${blog.blog_id}" class="btn btn-sm btn-outline-primary" onclick="updateBlogStatus(${blog.blog_id}, true)">Approve</button>
                        <button id="disapproveBTN_${blog.blog_id}" class="btn btn-sm btn-outline-danger" onclick="updateBlogStatus(${blog.blog_id}, false)">Disapprove</button>