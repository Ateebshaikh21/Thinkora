#!/bin/bash

# Thinkora Deployment Script
# This script helps you deploy Thinkora to various platforms

echo "🚀 Thinkora Deployment Helper"
echo "=============================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

# Main menu
echo "Select deployment platform:"
echo "1) Vercel (Frontend) + Render (Backend) - Recommended"
echo "2) Railway (Full Stack)"
echo "3) Build for production (manual deployment)"
echo "4) Docker build"
echo "5) Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        print_info "Deploying to Vercel + Render..."
        echo ""
        echo "Step 1: Deploy Backend to Render"
        echo "  1. Go to https://render.com"
        echo "  2. Click 'New +' → 'Web Service'"
        echo "  3. Connect your GitHub repository"
        echo "  4. Use these settings:"
        echo "     - Build Command: cd backend && pip install -r requirements.txt"
        echo "     - Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT"
        echo ""
        read -p "Press Enter when backend is deployed..."
        
        echo ""
        echo "Step 2: Deploy Frontend to Vercel"
        echo "  1. Go to https://vercel.com"
        echo "  2. Click 'New Project'"
        echo "  3. Import your GitHub repository"
        echo "  4. Use these settings:"
        echo "     - Framework: Vite"
        echo "     - Root Directory: frontend"
        echo "     - Build Command: npm run build"
        echo "     - Output Directory: dist"
        echo ""
        print_success "Deployment guide displayed!"
        ;;
        
    2)
        print_info "Deploying to Railway..."
        echo ""
        echo "1. Go to https://railway.app"
        echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "3. Select your repository"
        echo "4. Railway will auto-detect and deploy both services"
        echo ""
        print_success "Deployment guide displayed!"
        ;;
        
    3)
        print_info "Building for production..."
        
        # Build frontend
        echo ""
        print_info "Building frontend..."
        cd frontend
        npm install
        npm run build
        if [ $? -eq 0 ]; then
            print_success "Frontend built successfully! Output in frontend/dist/"
        else
            print_error "Frontend build failed!"
            exit 1
        fi
        cd ..
        
        # Check backend dependencies
        echo ""
        print_info "Checking backend dependencies..."
        cd backend
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            print_success "Backend dependencies installed!"
        else
            print_error "Backend dependency installation failed!"
            exit 1
        fi
        cd ..
        
        print_success "Production build complete!"
        echo ""
        echo "Next steps:"
        echo "  - Upload frontend/dist/ to your web server"
        echo "  - Deploy backend/ to your Python server"
        echo "  - Update environment variables"
        ;;
        
    4)
        print_info "Building Docker images..."
        
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            print_error "Docker is not installed. Please install Docker first."
            exit 1
        fi
        
        # Build backend
        echo ""
        print_info "Building backend Docker image..."
        cd backend
        docker build -t thinkora-backend .
        if [ $? -eq 0 ]; then
            print_success "Backend image built: thinkora-backend"
        else
            print_error "Backend Docker build failed!"
            exit 1
        fi
        cd ..
        
        # Build frontend
        echo ""
        print_info "Building frontend Docker image..."
        cd frontend
        docker build -t thinkora-frontend .
        if [ $? -eq 0 ]; then
            print_success "Frontend image built: thinkora-frontend"
        else
            print_error "Frontend Docker build failed!"
            exit 1
        fi
        cd ..
        
        print_success "Docker images built successfully!"
        echo ""
        echo "Run with: docker-compose up -d"
        ;;
        
    5)
        print_info "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid choice!"
        exit 1
        ;;
esac

echo ""
print_success "Done! Check DEPLOYMENT_GUIDE.md for detailed instructions."
