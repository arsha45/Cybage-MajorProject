import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  user = {
    username: '',
    email: '',
    password: '',
    password2: ''
  };

  constructor(private apiService: ApiService, private router: Router, private toastr: ToastrService) { }

  isPasswordValid(password: string): boolean {
    const passwordPattern = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{5,20}$/;
    return passwordPattern.test(password);
  }

  doPasswordsMatch(): boolean {
    return this.user.password === this.user.password2;
  }

  onSubmit() {
    if (!this.isPasswordValid(this.user.password)) {
      this.toastr.error('Password must contain at least one digit, one special character, one lowercase letter, one uppercase letter, and be between 5 and 20 characters.');
      return;
    }

    if (!this.doPasswordsMatch()) {
      this.toastr.error('Passwords do not match.');
      return;
    }

    this.apiService.register(this.user).subscribe(
      (data: any) => {
        console.log(data);
        this.toastr.success('Registered Successfully - Your request has been sent for approval !');
        this.router.navigate(['/login']); // Redirect to login
      },
      (error: any) => {
        console.error(error);
        if (error.status === 400) {
          if (error.error.username) {
            this.toastr.error('Username is already taken.');
          }
          if (error.error.email) {
            this.toastr.error('Please check your email');
          }
        } else {
          this.toastr.error('An error occurred during registration.');
        }
      }
    );
  }
}
