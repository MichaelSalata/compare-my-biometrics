TFVARS_FILE=../terraform/terraform.tfvars

instance_zone=$(grep '^zone' "$TFVARS_FILE" | awk -F'=' '{print $2}' | tr -d ' "')
instance_name=$(grep '^instance_name' "$TFVARS_FILE" | awk -F'=' '{print $2}' | tr -d ' "')

EXTERNAL_IP=$(gcloud compute instances describe $instance_name \
--zone="$instance_zone" \
--format='get(networkInterfaces[0].accessConfigs[0].natIP)')

if [ -n "$EXTERNAL_IP" ]; then
    # Construct the URL
    URL="http://$EXTERNAL_IP:8080"

    echo "Opening $URL in your default browser..."

    if command -v xdg-open > /dev/null; then
        # Linux
        xdg-open "$URL"
    elif command -v open > /dev/null; then
        # macOS
        open "$URL"
    elif command -v powershell.exe > /dev/null; then
        # WSL
        powershell.exe start "$URL"
    else
        echo "Could not detect the OS/browser opener. Please manually open: $URL"
    fi
else
    echo "Failed to retrieve the external IP. Please check your VM configuration."
fi

